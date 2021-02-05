"""Telegram Ping/Ping speed

Syntax: /ping
"""
import time

from pyrogram import emoji, filters

from telebot import Telebot, Config
from telebot.plugins.help import add_command_help


@Telebot.on_message(filters.command('ping', Config.COMMAND_HANDLER))
async def ping(_, message):
    start = time.time()
    rm = await message.reply_text("...")
    end = time.time()
    duration = (end - start) * 1000
    await rm.edit(f"{emoji.WHITE_SMALL_SQUARE} Pong!\n{duration:.3f} ms")

# Command help section
add_command_help('ping', [[f'{Config.COMMAND_HANDLER}ping', 'Ping/pong.']])
