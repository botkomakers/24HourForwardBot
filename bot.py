import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import yt_dlp
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
SONG_DIR = '/tmp/'  # Folder to store downloaded songs
STATUS_LIST = ['Love', 'Sad', 'Motivation']  # Can be expanded

# Sample jokes and shayari
JOKES = ['Why did the scarecrow win an award? Because he was outstanding in his field!', 'Knock Knock... Who’s there? Lettuce. Lettuce who? Lettuce in, it’s freezing out here!']
SHAYARI = ['तेरा नाम लूँ जुबां से, खुदा से यही दुआ है', 'अगर तुम खुद से खुश नहीं रह सकते तो दुनिया से क्या उम्मीद रखोगे।']

# Function to handle the start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your All-in-One Bot! Use the commands below:\n\n'
                              '/song <song name> - Download a song\n'
                              '/joke - Get a funny joke\n'
                              '/shayari - Get a beautiful Shayari\n'
                              '/status <love/sad/motivation> - Get a status\n'
                              '/reel - Get a random reel')

# Function to download song
def download_song(update: Update, context: CallbackContext) -> None:
    song_name = ' '.join(context.args)
    if not song_name:
        update.message.reply_text('Please provide a song name after the command: /song <song name>')
        return

    # Song download logic using yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{SONG_DIR}%(title)s.%(ext)s',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{song_name}", download=True)
        video = info_dict['entries'][0]
        song_file = f"{SONG_DIR}{video['title']}.mp3"
    
    # Send song file
    with open(song_file, 'rb') as song:
        update.message.reply_audio(song)

# Function to return a random joke
def joke(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(random.choice(JOKES))

# Function to return a random Shayari
def shayari(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(random.choice(SHAYARI))

# Function to return a status
def status(update: Update, context: CallbackContext) -> None:
    if not context.args or context.args[0].lower() not in ['love', 'sad', 'motivation']:
        update.message.reply_text(f"Please specify a valid status: {', '.join(STATUS_LIST)}")
        return
    status_type = context.args[0].lower()
    if status_type == 'love':
        update.message.reply_text('Love is when the other person’s happiness is more important than your own.')
    elif status_type == 'sad':
        update.message.reply_text('It’s okay to be sad sometimes. Embrace it and grow stronger.')
    elif status_type == 'motivation':
        update.message.reply_text('Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.')

# Function to send a random reel link (stub)
def reel(update: Update, context: CallbackContext) -> None:
    reels = ['https://www.instagram.com/reel/CjA4Yt4pDhT/', 'https://www.tiktok.com/@user/video/1234567890']
    update.message.reply_text(f"Here’s a random reel for you: {random.choice(reels)}")

# Main function to set up the bot
def main():
    # Set up the Updater and Dispatcher
    updater = Updater("7980272351:AAF4Ck8oAD8PYrSmRZpDUtITkxTpe2b6XrE")  # <-- Here, replace your token

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('song', download_song))
    dispatcher.add_handler(CommandHandler('joke', joke))
    dispatcher.add_handler(CommandHandler('shayari', shayari))
    dispatcher.add_handler(CommandHandler('status', status))
    dispatcher.add_handler(CommandHandler('reel', reel))

    # Start the bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()