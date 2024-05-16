from types import NoneType
from pyrogram import Client, filters
from pyrogram import *
from pytube import YouTube
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import random

global LINK
api_id = 1
api_hash = ""
bot_token = ""
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
LINK = None 
EMOJIS = ["🔥","🍬","🌹","🎂","👀","😜","🎶"]

def create_resolution_buttons(resolutions):
    keyboard = []
    for resolution in resolutions:
        keyboard.append([InlineKeyboardButton(f"{random.choice(EMOJIS)} {resolution}", callback_data=resolution)])
    return InlineKeyboardMarkup(keyboard)

async def download_and_send_video(bot, message, resolution):
    try:
        link = message.text
        yt = YouTube(link)
        video = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        video.download(filename='video.mp4')
        await bot.send_video(chat_id=message.chat.id, video='video.mp4', caption="**Video downloaded!**")
        os.remove('video.mp4')
    except Exception as e:
        await message.reply("**Error!** __Check console.__")
   
@app.on_message(filters.command("start"))
async def start(bot, message):
    await bot.send_message(chat_id=message.chat.id, text="**Hello!** __Send me a YouTube link!__")

@app.on_message(filters.text)
async def handle_link(bot, message):
    if "https://www.youtube.com/" in message.text or "https://www.youtu.be/" in message.text:
        global LINK
        LINK = message
        yt = YouTube(LINK.text)
        resolutions = [stream.resolution for stream in yt.streams.filter(progressive=True, file_extension='mp4')]
        resolution_buttons = create_resolution_buttons(resolutions)
        await bot.send_message(chat_id=message.chat.id, text="Pick a resolution:", reply_markup=resolution_buttons)

@app.on_callback_query()
async def callback(bot, update):
    resolution = update.data
    message = LINK
    await update.message.delete()
    await update.message.reply("Downloading...")
    await download_and_send_video(bot, message, resolution)

app.run()
idle()
