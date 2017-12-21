"""Get report from Stackalytics
/stackalytics - Get report from Stackalytics

- Just type /stackalytics without any additional options.
- Firstly, need to upload config file with json format:

For e.x:
    {
        "company": "Fujitsu",
        "members": [
            "kiennt26",
            "daidv"
        ]
    }
"""
import json
import logging
import urllib.error
import urllib.request

from telegram import ParseMode

from telebot import emojies
from telebot import utils

LOG = logging.getLogger(__name__)


def query(bot, update, user_id=None, company=None):
    """Query to http://stackalytics.com/"""
    url = 'http://stackalytics.com/api/1.0/contribution?'

    if company:
        url += 'company={}' . format(company)
    if user_id:
        url += '&user_id={}' . format(user_id)

    LOG.debug('Query url: {}' . format(url))

    try:
        stats = urllib.request.urlopen(url)
        stats = json.loads(stats.read().decode())
    except ValueError as e:
        msg = 'Error with JSON format: {}' . format(e)
        utils.handle_error(LOG, bot, update.message.chat_id, msg)
        return None
    except urllib.error.HTTPError as e:
        msg = 'Error when query member {}\'s stats: {}' . format(user_id, e)
        utils.handle_error(LOG, bot, update.message.chat_id, msg)
        return None
    patches = stats['contribution']['patch_set_count']
    commits = stats['contribution']['commit_count']
    reviews = \
        stats['contribution']['marks']['1'] + \
        stats['contribution']['marks']['-1'] + \
        stats['contribution']['marks']['2'] + \
        stats['contribution']['marks']['-2']
    return (patches, commits, reviews)


def handle(bot, update):
    try:
        config = json.load(open('/tmp/stackalyticsconfig.json'))
    except FileNotFoundError:
        msg = 'Config file doesn\' exist! Type /hep stackalytics again to \
               check usage!'
        utils.handle_error(LOG, bot, update.message.chat_id, msg)
        return
    except json.decoder.JSONDecodeError:
        msg = 'Wrong format! Type /hep stackalytics again to \
              check right format!'
        utils.handle_error(LOG, bot, update.message.chat_id, msg)
        return

    text = '{} *Report:*\n' . format(emojies.point_right) 
    template = '- Member `{}`: `{}` patches, `{}` commits, `{}` reviews.\n'
    for member in config['members']:
        results = query(bot, update,
                        user_id=member,
                        company=config['company'])
        if not results:
            continue

        patches, commits, reviews = results
        text += template.format(member, patches, commits, reviews)
    bot.send_message(chat_id=update.message.chat_id,
                     text=text,
                     parse_mode=ParseMode.MARKDOWN)
