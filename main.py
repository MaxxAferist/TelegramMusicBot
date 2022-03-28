from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from tokens import BOT_TOKEN, GENIUS_TOKEN
import lyricsgenius as lg
import requests


def start(update, context):
    pass


def stop(update, context):
    pass


def search_song(update, context):
    genius = lg.Genius(GENIUS_TOKEN)
    song = genius.search_song(update.message.text)
    update.message.reply_text(song.lyrics)


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~ Filters.command, search_song, pass_user_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
