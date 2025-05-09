import os
import logging
import yt_dlp
import random
import nest_asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    Application, Dispatcher, CommandHandler, MessageHandler,
    CallbackContext, ContextTypes, filters
)

nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Render env var
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # eg. https://your-app.onrender.com

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

SONG_DIR = "/tmp/"
STATUS_LIST = ['Love', 'Sad', 'Motivation']
JOKES = ['Why did the scarecrow win an award? Because he was outstanding in his field!', 'Knock Knock... Who’s there? Lettuce. Lettuce who? Lettuce in, it’s freezing out here!']
SHAYARI = ['तेरा नाम लूँ जुबां से, खुदा से यही दुआ है', 'अगर तुम खुद से खुश नहीं रह सकते तो दुनिया से क्या उम्मीद रखोगे।']

# Handler functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am your All-in-One Bot!\n\n"
        "/song <song name> - Download a song\n"
        "/joke - Get a funny joke\n"
        "/shayari - Get a beautiful Shayari\n"
        "/status <love/sad/motivation> - Get a status\n"
        "/reel - Get a random reel"
    )

async def download_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    song_name = ' '.join(context.args)
    if not song_name:
        await update.message.reply_text('Please provide a song name after the command: /song <song name>')
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{SONG_DIR}%(title)s.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
        video = info['entries'][0]
        file_path = f"{SONG_DIR}{video['title']}.mp3"

    with open(file_path, 'rb') as song:
        await update.message.reply_audio(song)

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(JOKES))

async def shayari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(SHAYARI))

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0].lower() not in ['love', 'sad', 'motivation']:
        await update.message.reply_text(f"Please specify a valid status: {', '.join(STATUS_LIST)}")
        return
    msg = {
        'love': 'Love is when the other person’s happiness is more important than your own.',
        'sad': 'It’s okay to be sad sometimes. Embrace it and grow stronger.',
        'motivation': 'Believe in yourself and all that you are. You’re greater than any obstacle.'
    }
    await update.message.reply_text(msg[context.args[0].lower()])

async def reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reels = ['https://www.instagram.com/reel/CjA4Yt4pDhT/', 'https://www.tiktok.com/@user/video/1234567890']
    await update.message.reply_text(f"Here’s a random reel for you: {random.choice(reels)}")

# Flask Routes
@app.route('/')
def index():
    return "Bot is Alive!"

@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.update_queue.put(update)
    return "ok"

@app.before_first_request
def init_webhook():
    bot.delete_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")

# Create Telegram Application
application = Application.builder().token(BOT_TOKEN).build()

# Register handlers
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('song', download_song))
application.add_handler(CommandHandler('joke', joke))
application.add_handler(CommandHandler('shayari', shayari))
application.add_handler(CommandHandler('status', status))
application.add_handler(CommandHandler('reel', reel))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run_task()  # Start background application loop
    app.run(host="0.0.0.0", port=port)