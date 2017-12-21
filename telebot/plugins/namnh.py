"""A joke about my colleague - NamNH :lmao:
/namnh - Chot Chat command
"""
from telebot import emojies


def handle(bot, update):
    msg = '{} Typo! On fire! {}' . format(emojies.fire, emojies.fire)
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)
    bot.send_sticker(chat_id=update.message.chat_id,
                     caption='Chotchat',
                     sticker=open('/tmp/namnh.jpg', 'rb'))
