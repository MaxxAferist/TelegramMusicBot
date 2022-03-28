from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from tokens import BOT_TOKEN, GENIUS_TOKEN, CLIENT_ID, CLIENT_SECRET
import lyricsgenius as lg
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import re


def start(update, context):
    pass


def stop(update, context):
    pass


def search_song(update, context):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                               client_secret=CLIENT_SECRET))
    genius = lg.Genius(GENIUS_TOKEN)
    song = genius.search_song(update.message.text)
    text = f'{song.artist} {song.title}'
    text = re.sub(r'\([^()]*\)', '', text)
    result = sp.search(q=text)['tracks']['items'][0]['external_urls']['spotify']
    update.message.reply_text(song.lyrics)
    update.message.reply_text(f"Spotify: {result}")


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~ Filters.command, search_song, pass_user_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
