__all__ = ['Config']

import os

from telebot import logging

LOG = logging.getLogger(__name__)


class Config:
    """Config to setup Telebot"""
    # Get these values from my.telegram.org
    API_ID = int(os.environ.get('API_ID'))
    API_HASH = os.environ.get('API_HASH')
    # Get Bot token by chatting with @botfather
    BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # specify command handler that should be used for the plugins
    # this should be a valid "regex" pattern
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", "/")
    # This is required for the plugins involving the file system.
    TMP_DIR = os.environ.get(
        "TMP_DIR",
        "./temp"
    )
    # For Databases
    # can be None in which case plugins requiring
    # DataBase would not work
    DB_URI = os.environ.get("DATABASE_URL", None)
