import logging
import sys

from telebot import emojies


def handle_error(logger, bot, chat_id, msg):
    logger.error(msg)
    msg = '{} {}' . format(emojies.skull, msg)
    bot.send_message(chat_id=chat_id,
                     text=msg)


def init_log(config):
    stream = config.get('logstream', False)
    logfile = config.get('logfile', '/var/log/telebot.log')
    loglevel = config.get('loglevel', logging.INFO)
    logformat = config.get(
        'logformat',
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if not stream:
        logging.basicConfig(filename=logfile,
                            format=logformat, level=loglevel)
    else:
        logging.basicConfig(format=logformat, level=loglevel,
                            stream=sys.stdout)
