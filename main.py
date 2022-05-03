from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, User
from tokens import BOT_TOKEN, GENIUS_TOKEN, CLIENT_ID, CLIENT_SECRET
import lyricsgenius as lg
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import re
import flask_app
from data.users import User
from data.songs import Song
from data.authors import Author
from data.searches import Search
import logging
import json
import threading
import random
from list_anekdotov import anekdoty


def stop(update, context):
    update.message.reply_text(
        "Конец работы. Регистрация сбросилась."
    )
    return ConversationHandler.END


def process_search(update, context):
    try:
        update.message.reply_text('Ищем...')
        song_text = update.message.text
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                                   client_secret=CLIENT_SECRET))
        genius = lg.Genius(GENIUS_TOKEN)
        song = genius.search_song(song_text)
        text = f'{song.artist} {song.title}'
        text = re.sub(r'\([^()]*\)', '', text)
        # result = sp.search(q=text)['tracks']['items'][0]
        # url = result['external_urls']['spotify']
        url = 'В данный момент Spotify не работает на территории России из-за санкций\nПриносим свои извинения'

        context.user_data['title'] = song.title
        context.user_data['artist'] = song.artist
        context.user_data['lyrics'] = song.lyrics
        context.user_data['url'] = url

        user_id = context.user_data.get('user_id')

        push_json = {'title': song.title,
                     'artist': song.artist,
                     'url': url
                     }
        resp = requests.post(
            'http://localhost:8000/api/song/add_searches', json=push_json).json()
        song_id = resp.get('song_id')

        push_json = {'artist': song.artist}
        requests.post(
            'http://localhost:8000/api/authors/add_searhes', json=push_json)

        push_json = {'user_id': user_id,
                     'song_id': song_id,
                     'success': False
                     }
        if context.user_data.get('success'):
            push_json['success'] = True
        requests.post(
            'http://localhost:8000/api/searches/add', json=push_json)
        
        keyboard = [['Текст песни', 'Ссылку на песню'],
                    ['Название', 'Автор'],
                    ['Найти другую', 'Выйти']]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        update.message.reply_text('Песня найдена... Что хотите увидеть?',
                                  reply_markup=markup)
        return 0
    except IndexError as e:
        update.message.reply_text('Песня не найдена. Попробуйте снова!')
        return 1
    except TypeError:
        update.message.reply_text('Песня не найдена. Попробуйте снова!')
        return 1
    except AttributeError:
        update.message.reply_text('Песня не найдена. Попробуйте снова!')
        return 1
    except Exception as e:
        print(e.__class__.__name__)
        update.message.reply_text('Произошла ошибка')
        return 1


def handler(update, context):
    answer = update.message.text.lower()
    if answer in ['поиск', 'найти другую']:
        update.message.reply_text(
            "Введите строку из песни"
        )
        return 1
    elif answer == 'ссылка на сайт':
        reply_keyboard = [['Поиск', 'Ссылка на сайт'],
                          ['Регистрация', 'Войти']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Ссылка на сайт",
            reply_markup=markup
        )
        return 0
    elif answer == 'регистрация':
        update.message.reply_text('Напишите имя пользователя')
        return 2
    elif answer == 'войти':
        update.message.reply_text('Напишите имя пользователя')
        return 3
    elif answer == 'текст песни':
        keyboard = [['Текст песни', 'Ссылку на песню'],
                    ['Название', 'Автор'],
                    ['Найти другую', 'Выйти']]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        update.message.reply_text(
            context.user_data["lyrics"], reply_markup=markup)
        return 0
    elif answer == 'ссылку на песню':
        keyboard = [['Текст песни', 'Ссылку на песню'],
                    ['Название', 'Автор'],
                    ['Найти другую', 'Выйти']]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        update.message.reply_text(
            context.user_data["url"], reply_markup=markup)
        return 0
    elif answer == 'название':
        keyboard = [['Текст песни', 'Ссылку на песню'],
                    ['Название', 'Автор'],
                    ['Найти другую', 'Выйти']]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        update.message.reply_text(
            context.user_data["title"], reply_markup=markup)
        return 0
    elif answer == 'автор':
        keyboard = [['Текст песни', 'Ссылку на песню'],
                    ['Название', 'Автор'],
                    ['Найти другую', 'Выйти']]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        update.message.reply_text(
            context.user_data["artist"], reply_markup=markup)
        return 0
    elif answer == 'выйти':
        reply_keyboard = [['Поиск', 'Ссылка на сайт'],
                          ['Регистрация', 'Войти']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        if context.user_data.get("success"):
            update.message.reply_text(
                "Вы можете посмотреть историю на сайте!",
                reply_markup=markup
            )
        else:
            update.message.reply_text(
                "Зарегистрируйтесь, чтобы не потерять историю пойска!",
                reply_markup=markup
            )
        return 0
    elif answer == 'анекдот':
        anek = anekdoty[random.randrange(0, len(anekdoty))]
        update.message.reply_text(anek)


def registration(update, context):
    if not context.user_data.get("name"):
        name = update.message.text
        push_json = {'name': name}
        resp = requests.post(
            'http://localhost:8000/api/register/name', json=push_json).json()
        msg = resp.get('message')
        if msg == 'success':
            context.user_data["name"] = name
            update.message.reply_text('Введите пароль')
            return 2
        update.message.reply_text(msg)
        return 2
    if not context.user_data.get("password"):
        password = update.message.text
        context.user_data["password"] = password
        update.message.reply_text('Введите пароль ещё раз')
        return 2
    if not context.user_data.get("password_again"):
        password_again = update.message.text
        context.user_data["password_again"] = password_again
        if context.user_data["password"] == context.user_data["password_again"]:
            context.user_data["success"] = True
            push_json = {'name': context.user_data["name"],
                         'password': context.user_data["password"]
                         }
            resp = requests.post(
                'http://localhost:8000/api/register/user', json=push_json).json()
            user_id = resp["user_id"]
            context.user_data["user_id"] = user_id
            reply_keyboard = [['Поиск', 'Ссылка на сайт'],
                              ['Регистрация', 'Войти']]
            markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)
            update.message.reply_text(
                'Вы успешно зарегистрированны! Теперь можете войти на наш сайт и просматривать свою историю', reply_markup=markup)
            return 0
        else:
            reply_keyboard = [['Поиск', 'Ссылка на сайт'],
                              ['Регистрация', 'Войти']]
            markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)
            update.message.reply_text(
                "Неправильный пароль", reply_markup=markup)
        context.user_data["name"] = None
        context.user_data["password"] = None
        context.user_data["password_check"] = None
        return 0
    else:
        update.message.reply_text('Вы уже зарегистрированы!')
        return 0


def login(update, context):
    if not context.user_data.get("login_name"):
        name = update.message.text

        push_json = {'name': name}
        resp = requests.post(
            'http://localhost:8000/api/login/name', json=push_json).json()
        msg = resp.get('message')
        if msg == 'success':
            context.user_data["login_name"] = name
            update.message.reply_text('Введите пароль')
            return 3
        update.message.reply_text(msg)
        return 3
    if not context.user_data.get("login_password"):
        password = update.message.text
        login_name = context.user_data["login_name"]
        push_json = {'password': password,
                     'login_name': login_name}

        resp = requests.post(
            'http://localhost:8000/api/login/password', json=push_json).json()
        is_auth = resp.get('result')
        if is_auth:
            user_id = resp.get('user_id')
            context.user_data["success"] = True
            context.user_data["user_id"] = user_id
            reply_keyboard = [['Поиск', 'Ссылка на сайт'],
                              ['Регистрация', 'Войти']]
            markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)
            update.message.reply_text(
                'Вы успешно вошли!', reply_markup=markup)
            context.user_data["login_password"] = password
        else:
            reply_keyboard = [['Поиск', 'Ссылка на сайт'],
                              ['Регистрация', 'Войти']]
            markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)
            update.message.reply_text(
                "Неправильный пароль", reply_markup=markup)
        context.user_data["name"] = None
        context.user_data["password"] = None
        context.user_data["password_check"] = None
        context.user_data["login_password"] = None
        context.user_data["login_name"] = None
        return 0


def start(update, context):
    reply_keyboard = [['Поиск', 'Ссылка на сайт'],
                      ['Регистрация', 'Войти']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет, вы попали в MusicBot\n"
        "С его помощью можно найти любую песню по строке из неё\n"
        "p.s. Введя 'Анекдот' Вы получите смешные анекдоты",
        reply_markup=markup
    )


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(
            Filters.text & ~ Filters.command, handler)],
        states={
            0: [MessageHandler(Filters.text & ~ Filters.command, handler,
                               pass_user_data=True)],
            1: [MessageHandler(Filters.text & ~ Filters.command, process_search, pass_user_data=True)],
            2: [MessageHandler(Filters.text & ~ Filters.command, registration, pass_user_data=True)],
            3: [MessageHandler(Filters.text & ~ Filters.command, login,
                               pass_user_data=True)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    app = flask_app.App()
    app.activate_route()
    t1 = threading.Thread(target=app.run)
    t1.start()
    main()
