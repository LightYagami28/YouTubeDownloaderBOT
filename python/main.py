from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube
import os
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Configuration
api_id = 1
api_hash = ""
bot_token = ""
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
LINK = None
EMOJIS = ["🔥", "🍬", "🌹", "🎂", "👀", "😜", "🎶"]

# Create resolution buttons for inline keyboard
def create_resolution_buttons(resolutions):
    keyboard = [[InlineKeyboardButton(f"{random.choice(EMOJIS)} {res}", callback_data=res)] for res in resolutions]
    return InlineKeyboardMarkup(keyboard)

# Download and send video
async def download_and_send_video(bot, chat_id, link, resolution):
    try:
        yt = YouTube(link)
        video = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        video_path = os.path.join(os.getcwd(), 'video.mp4')
        video.download(filename=video_path)
        with open(video_path, 'rb') as video_file:
            await bot.send_video(chat_id=chat_id, video=video_file, caption="**Video downloaded!**")
        os.remove(video_path)
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        await bot.send_message(chat_id=chat_id, text="**Error!** __Check console.__")

# Start command
@app.on_message(filters.command("start"))
async def start(bot, message):
    await bot.send_message(chat_id=message.chat.id, text="**Hello!** __Send me a YouTube link!__")

# Handle YouTube link
@app.on_message(filters.text)
async def handle_link(bot, message):
    if "https://www.youtube.com/" in message.text or "https://youtu.be/" in message.text:
        global LINK
        LINK = message.text
        yt = YouTube(LINK)
        resolutions = list(set(stream.resolution for stream in yt.streams.filter(progressive=True, file_extension='mp4')))
        resolution_buttons = create_resolution_buttons(resolutions)
        await bot.send_message(chat_id=message.chat.id, text="Pick a resolution:", reply_markup=resolution_buttons)

# Handle resolution selection
@app.on_callback_query()
async def callback(bot, update):
    resolution = update.data
    await update.message.delete()
    await update.message.reply("Downloading...")
    await download_and_send_video(bot, update.message.chat.id, LINK, resolution)

# Run the bot
app.run()
