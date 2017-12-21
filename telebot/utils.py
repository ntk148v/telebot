from telebot import emojies


def handle_error(logger, bot, chat_id, msg):
    logger.error(msg)
    msg = '{} {}' . format(emojies.skull, msg) 
    bot.send_message(chat_id=chat_id,
                     text=msg)
