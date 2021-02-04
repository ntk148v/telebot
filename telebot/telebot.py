from pyrogram import (
    Client,
    __version__
)
from pyrogram.errors import MessageNotModified
from pyrogram.raw.all import layer

class TeleBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            ":memory:",
            plugins=dict(root=f"{name}/plugins"),
            workdir=TMP_DOWNLOAD_DIRECTORY,
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_COMPANION_BOT
        )