"""Test plugin
/test - do nothing!
"""


def handle(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Just for testing')
