import logging
import os

from telebot import bot
from telebot import utils


def get_config():
    config = {}
    config['telegram_token'] = os.getenv('TELEGRAM_TOKEN')
    config['loglevel'] = os.getenv('TELEBOT_LOGLEVEL')
    config['logfile'] = os.getenv('TELEBOT_LOGFILE')
    config['logformat'] = os.getenv('TELEBOT_LOGFORMAT')
    return config


def main(args):
    config = get_config()
    if args.debug:
        config['loglevel'] = logging.DEBUG
    if args.logstream:
        config['logstream'] = True

    utils.init_log(config)

    try:
        BOT = bot.Bot(config['telegram_token'])
        BOT.run()
    except (KeyboardInterupt, SystemExit):
        BOT.stop()
