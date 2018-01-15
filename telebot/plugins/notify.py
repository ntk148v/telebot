"""Send a direct message to user if user's name was mentioned in a group/channel.
This plugin is to notification to user who is tagged. And this plugin need to
have a configuration yaml file as template:

For example:
[
    {"name": "@namnh307", "id": "473649555"},
    {"name": "@daidv", "id": "432649532"}
]
"""

import logging
import json

LOG = logging.getLogger(__name__)


def check_messsage(users, message):
    return [user['id'] for user in users if user['name'] in message]


def handle(bot, update):
    try:
        config_user = json.load(open('/tmp/config_user.json'))
    except FileNotFoundError:
        LOG.warning('There is no the config_user.json at all')
        return
    user_ids = check_messsage(config_user, update.message.text)
    if user_ids:
        msg = 'You have a message from: {0} with content: {1}'.format(
            update.message.from_user.username,
            update.message.text
        )
        for user_id in user_ids:
            bot.send_message(chat_id=user_id, text=msg)
