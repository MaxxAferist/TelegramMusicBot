from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from tokens import BOT_TOKEN
import requests


def start(update, context):
    pass


def stop(update, context):
    pass


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
