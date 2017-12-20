import logging
import os

from telebot import bot

LOG = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()])
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    BOT = bot.Bot(TELEGRAM_TOKEN)
    BOT.run()
    LOG.info('Bot started!')
