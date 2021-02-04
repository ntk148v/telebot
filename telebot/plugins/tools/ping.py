"""Telegram Ping/Ping speed

Syntax: /ping
"""
import time

from pyrogram import Client, emoji, filters

from telebot.config import Config


@Client.on_message(filters.command('ping', Config.COMMAND_HANDLER))
async def ping(_, message):
    start = time.time()
    rm = await message.reply_text("...")
    end = time.time()
    duration = (end - start) * 1000
    await rm.edit(f"{emoji.WHITE_SMALL_SQUARE} Pong!\n{duration:.3f} ms")
