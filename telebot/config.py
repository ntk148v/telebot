import os
import logging

from dotenv import load_dotenv

LOG = logging.getLogger(__name__)

load_dotenv()
class Config:
    """Config to setup Telebot"""
    # Get these values from my.telegram.org
    API_ID = int(os.environ.get('API_ID'))
    API_HASH = os.environ.get('API_HASH')
    # Get Bot token by chatting with @botfather
    BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # Number of maximum concurrent workers for handling incoming updates.
    WORKERS = int(os.environ.get('WORKERS')) or os.cpu_count() + 4
    # Pass a string of your choice to give a name to the client session
    BOT_SESSION = os.environ.get('BOT_SESSION', ':memory:')
    # specify command handler that should be used for the plugins
    # this should be a valid "regex" pattern
    COMMAND_HANDLER = os.environ.get('COMMAND_HANDLER', '/')
    # Define a custom working directory. The working directory is
    # the location in your filesystem where Pyrogram
    # will store your session files.
    WORK_DIR = os.environ.get(
        "WORK_DIR",
        "/tmp/telebot/"
    )
    # The parse mode, can be any of: *"combined"*,
    # for the default combined mode. *"markdown"* or *"md"*
    # to force Markdown-only styles. *"html"* to force HTML-only
    # styles. *None* to disable the parser completely.
    PARSE_MODE = os.environ.get('PARSE_MODE', 'combined')
    # For Databases
    # can be None in which case plugins requiring
    # DataBase would not work
    DATABASE_URL = os.environ.get('DATABASE_URL', None)
