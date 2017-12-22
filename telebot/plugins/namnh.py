"""A joke about my colleague - NamNH :lmao:
/namnh - Chot Chat command
"""
import os
from telebot import emojies

PARDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
IMG = PARDIR + '/imgs/namnh.jpg'


def handle(bot, update):
    msg = '{} Typo! On fire! {}' . format(emojies.fire, emojies.fire)
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)
    bot.send_sticker(chat_id=update.message.chat_id,
                     caption='Chotchat',
                     sticker=open(IMG, 'rb'))
    return
