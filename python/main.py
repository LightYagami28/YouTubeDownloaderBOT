from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube
import os
import random
import logging
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Recupera le variabili d'ambiente
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Verifica che tutte le variabili d'ambiente siano state caricate
if not all([api_id, api_hash, bot_token]):
    raise ValueError("Le variabili d'ambiente API_ID, API_HASH e BOT_TOKEN devono essere impostate nel file .env")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Crea l'istanza del Client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
LINK = None
EMOJIS = ["🔥", "🍬", "🌹", "🎂", "👀", "😜", "🎶"]

# Crea i pulsanti di risoluzione per la tastiera inline
def create_resolution_buttons(resolutions):
    keyboard = [[InlineKeyboardButton(f"{random.choice(EMOJIS)} {res}", callback_data=res)] for res in resolutions]
    return InlineKeyboardMarkup(keyboard)

# Scarica e invia il video
async def download_and_send_video(bot, chat_id, link, resolution):
    try:
        yt = YouTube(link)
        video = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        if not video:
            await bot.send_message(chat_id=chat_id, text="**Error!** __Video not found.__")
            return
        video_path = os.path.join(os.getcwd(), 'video.mp4')
        video.download(filename=video_path)
        with open(video_path, 'rb') as video_file:
            await bot.send_video(chat_id=chat_id, video=video_file, caption="**Video downloaded!**")
        os.remove(video_path)
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        await bot.send_message(chat_id=chat_id, text="**Error!** __Check console.__")

# Comando start
@app.on_message(filters.command("start"))
async def start(bot, message):
    await bot.send_message(chat_id=message.chat.id, text="**Hello!** __Send me a YouTube link!__")

# Gestisci il link di YouTube
@app.on_message(filters.text)
async def handle_link(bot, message):
    if "https://www.youtube.com/" in message.text or "https://youtu.be/" in message.text:
        global LINK
        LINK = message.text
        try:
            yt = YouTube(LINK)
            resolutions = list(set(stream.resolution for stream in yt.streams.filter(progressive=True, file_extension='mp4')))
            if not resolutions:
                await bot.send_message(chat_id=message.chat.id, text="**Error!** __No suitable resolutions found.__")
                return
            resolution_buttons = create_resolution_buttons(resolutions)
            await bot.send_message(chat_id=message.chat.id, text="Pick a resolution:", reply_markup=resolution_buttons)
        except Exception as e:
            logging.error(f"Error handling link: {e}")
            await bot.send_message(chat_id=message.chat.id, text="**Error!** __Check console.__")

# Gestisci la selezione della risoluzione
@app.on_callback_query()
async def callback(bot, update):
    resolution = update.data
    await update.message.delete()
    await update.message.reply("Downloading...")
    await download_and_send_video(bot, update.message.chat.id, LINK, resolution)

# Esegui il bot
app.run()
