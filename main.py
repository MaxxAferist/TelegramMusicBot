from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from tokens import BOT_TOKEN, GENIUS_TOKEN, CLIENT_ID, CLIENT_SECRET
import lyricsgenius as lg
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import re


def stop(update, context):
    update.message.reply_text(
        "Конец работы"
    )
    return ConversationHandler.END


def process_search(update, context):
    song_text = update.message.text
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                               client_secret=CLIENT_SECRET))
    genius = lg.Genius(GENIUS_TOKEN)
    song = genius.search_song(song_text)
    text = f'{song.artist} {song.title}'
    text = re.sub(r'\([^()]*\)', '', text)
    result = sp.search(q=text)['tracks']['items'][0]['external_urls']['spotify']
    update.message.reply_text(song.lyrics)
    update.message.reply_text(f"Spotify: {result}")
    return ConversationHandler.END


def search_song(update, context):
    answer = update.message.text
    if answer == 'Поиск':
        update.message.reply_text(
            "Введите строку из песни"
        )

        return 1
    elif answer == 'Стоп':
        stop(update, context)


def start(update, context):
    reply_keyboard = [['Поиск'], ['Стоп']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(
        "Привет, вы попали в MusicBot\n"
        "С его помощью можно найти любую песню по строке из неё",
        reply_markup=markup
    )


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text & ~ Filters.command, search_song)],

        states={
            1: [MessageHandler(Filters.text & ~ Filters.command, process_search, pass_user_data=True)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
