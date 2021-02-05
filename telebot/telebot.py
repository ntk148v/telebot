import logging

from pyrogram import (
    Client,
    __version__
)

from telebot.config import Config

LOG = logging.getLogger(__name__)


class Telebot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        LOG.info('Settings Telebot configs')
        kwargs = {}
        if Config.BOT_TOKEN:
            kwargs['bot_token'] = Config.BOT_TOKEN
        super().__init__(
            Config.USER_SESSION,
            plugins=dict(root=f"{name}/plugins"),
            workdir=Config.WORK_DIR,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            workers=Config.WORKERS,
            parse_mode=Config.PARSE_MODE,
            **kwargs)

    async def start(self):
        # Extend later
        LOG.info('Starting Telebot...')
        await super().start()
        LOG.info(f'Telebot based on Pyrogram v{__version__}. Say Hi!')

    async def stop(self, *args):
        # Extend later
        LOG.info('Stopping Telebot...')
        await super().stop()
        LOG.info('Telebot stopped. Bye...')
