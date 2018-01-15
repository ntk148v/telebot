import logging
import os

from telebot import bot


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

    # Logging not ready yet
    # utils.init_log(config)

    BOT = bot.Bot(config['telegram_token'])
    BOT.run()
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    BOT.idle()
