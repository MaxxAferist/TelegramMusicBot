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
from data import db_session
from data.users import User
from data.songs import Song
from data.authors import Author
from data.searches import Search
import logging
import json
import threading


def stop(update, context):
    update.message.reply_text(
        "Конец работы. Регистрация сбросилась."
    )
    return ConversationHandler.END


def process_search(update, context):
    try:
        song_text = update.message.text
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                                client_secret=CLIENT_SECRET))
        genius = lg.Genius(GENIUS_TOKEN)
        song = genius.search_song(song_text)
        text = f'{song.artist} {song.title}'
        text = re.sub(r'\([^()]*\)', '', text)
        result = sp.search(q=text)['tracks']['items'][0]
        url = result['external_urls']['spotify']

        context.user_data['title'] = song.title
        context.user_data['artist'] = song.artist
        context.user_data['lyrics'] = song.lyrics
        context.user_data['url'] = url
        db_sess = db_session.create_session()
        song_db = db_sess.query(Song).filter((Song.title == song.title) & (Song.artist == song.artist)).first()
        if song_db:
            song_db.searches += 1
        else:
            song_db = Song(
                title=song.title,
                artist=song.artist,
                url=url,
                searches=1
            )
            db_sess.add(song_db)
        author_db = db_sess.query(Author).filter(Author.name == song.artist).first()
        if author_db:
            author_db.searches += 1
        else:
            author_db = Author(
                name=song.artist,
                searches=1
            )
            db_sess.add(author_db)
        user_id = context.user_data.get('user_id')
        search = Search(
            user_id=user_id,
            song_id=song_db.id
            )
        db_sess.add(search)
        if context.user_data.get('success'):
            user = db_sess.query(User).filter(User.id == user_id).first()
            user.searches_id = str(user.searches_id) + ' ' + str(search.id)
        db_sess.commit()
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
    except Exception as e:
        print(e)
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


def registration(update, context):
    if not context.user_data.get("name"):
        name = update.message.text
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == name).first()
        if user:
            update.message.reply_text("Имя занято. Попробуйте другое!")
            return 2
        context.user_data["name"] = name
        update.message.reply_text('Введите пароль')
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
            db_sess = db_session.create_session()
            user = User()
            user.name = context.user_data["name"]
            user.set_password(context.user_data["password"])
            user.searches_id = ''
            db_sess.add(user)
            db_sess.commit()
            context.user_data["user_id"] = user.id
            reply_keyboard = [['Поиск', 'Ссылка на сайт'], ['Регистрация', 'Войти']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text('Вы успешно зарегистрированны! Теперь можете войти на наш сайт и просматривать свою историю', reply_markup=markup)
            return 0
        else:
            reply_keyboard = [['Поиск', 'Ссылка на сайт'],
                              ['Регистрация', 'Войти']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text("Неправильный пароль", reply_markup=markup)
        context.user_data["name"] = None
        context.user_data["password"] = None
        context.user_data["password_check"] = None
        return 0


def login(update, context):
    if not context.user_data.get("login_name"):
        name = update.message.text
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == name).first()
        if not user:
            update.message.reply_text("Такого пользователя не существует")
            return 3
        context.user_data["login_name"] = name
        update.message.reply_text('Введите пароль')
        return 3
    if not context.user_data.get("login_password"):
        password = update.message.text
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == context.user_data["login_name"]).first()
        if user.check_password(password):
            context.user_data["success"] = True
            db_sess.commit()
            context.user_data["user_id"] = user.id
            reply_keyboard = [['Поиск', 'Ссылка на сайт'], ['Регистрация', 'Войти']]
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
        "С его помощью можно найти любую песню по строке из неё",
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
    db_session.global_init("db/music.db")
    app = flask_app.App()
    app.activate_route()
    t1 = threading.Thread(target=app.run)
    t1.start()
    main()
