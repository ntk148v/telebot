import logging
from logging.handlers import RotatingFileHandler
import pathlib

from telebot.config import Config

# Create directory if not exist
pathlib.Path(f'{Config.WORK_DIR}/logs').mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    handlers=[
                        RotatingFileHandler(
                            f"{Config.WORK_DIR}/logs/telebot.log",
                            maxBytes=(20480), backupCount=10),
                        logging.StreamHandler()
                    ])

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.parser.html").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.ERROR)
