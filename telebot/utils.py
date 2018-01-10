import logging

from telebot import emojies


def handle_error(logger, bot, chat_id, msg):
    logger.error(msg)
    msg = '{} {}' . format(emojies.skull, msg)
    bot.send_message(chat_id=chat_id,
                     text=msg)


def init_log(config):
    stream = config.get('logstream', False)
    logfile = config.get('logfile', '/tmp/telebot.log')
    loglevel = config.get('loglevel', logging.INFO)
    logformat = config.get(
        'logformat',
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handlers = [logging.FileHandler(logfile, mode='wb')]
    if stream:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(format=logformat, level=loglevel,
                        handlers=handlers)
