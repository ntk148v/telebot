"""Echo plugin
/echo - do nothing!
"""


def handle(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Hey! I\'m Bot')
