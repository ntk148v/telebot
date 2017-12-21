def handle_error(logger, bot, chat_id, msg):
    logger.error(msg)
    bot.send_message(chat_id=chat_id,
                     text=msg)
