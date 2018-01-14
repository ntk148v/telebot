"""
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


def check_messsage(list_user, message):
    list_id = []
    for user in list_user:
        if user['name'] in message:
            list_id.append(user['id'])
    return list_id if len(list_id) != 0 else None


def handle(bot, update):
    try:
        config_user = json.load(open('/tmp/config_user.json'))
    except FileNotFoundError:
        LOG.warning('There is no the config_user.json at all')
        return
    list_id_user = check_messsage(config_user, update.message.text)
    if list_id_user is not None:
        msg = 'You have a message from: {0} with content: {1}'.format(
            update.message.from_user.username,
            update.message.text
        )
        for id_user in list_id_user:
            bot.send_message(chat_id=id_user, text=msg)
