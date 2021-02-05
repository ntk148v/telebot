import os
import re

import asyncio
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from pyrogram import filters
from pyrogram.types import Message

from telebot import Telebot, Config
from telebot.plugins.help import add_command_help


@Telebot.on_message(filters.command("lyrics", Config.COMMAND_HANDLER))
async def lyrics(_, message: Message):
    cmd = message.command
    message = await message.reply_text("...")
    if not (len(cmd) >= 2):
        await message.edit("```Bruh WTF? Input your damn song!```")
        await asyncio.sleep(3)
        await message.delete()
        return

    song = ' '.join(cmd[1:]).capitalize()
    await message.edit(f"__Searching Lyrics For {song}__")
    to_search = song + "genius lyrics"
    gen_surl = list(search(to_search, num_results=1))[0]
    gen_page = requests.get(gen_surl)
    scp = BeautifulSoup(gen_page.text, 'html.parser')
    lyrics = scp.find("div", class_="lyrics")
    if not lyrics:
        await message.edit(f"No Results Found for: `{song}`")
        return
    lyrics = lyrics.get_text()
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    lyrics = os.linesep.join((s for s in lyrics.splitlines() if s))
    title = scp.find('title').get_text().split("|")
    writers_box = [
        writer
        for writer in scp.find_all("span", {'class': 'metadata_unit-label'})
        if writer.text == "Written By"]
    if writers_box:
        target_node = writers_box[0].find_next_sibling(
            "span", {'class': 'metadata_unit-info'})
        writers = target_node.text.strip()
    else:
        writers = "UNKNOWN"
    lyr_format = ''
    lyr_format += '**' + title[0] + '**\n'
    lyr_format += '__' + lyrics + '__'
    lyr_format += "\n\n**Written By: **" + '__' + writers + '__'
    lyr_format += "\n**Source: **" + '`' + title[1] + '`'

    if lyr_format:
        await message.edit(lyr_format)
    else:
        await message.edit(f"No Lyrics Found for **{song}**")

add_command_help(
    "lyrics",
    [[f"{Config.COMMAND_HANDLER}lyrics songname",
        "Scrape Song Lyrics from Genius.com"]]
)
