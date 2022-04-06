from flask import Flask, abort, jsonify, make_response, redirect, request, render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from data import db_session
from data.searches import Search
from data.users import User
from data.songs import Song
from data.authors import Author
from forms.login import LoginForm
from flask_restful import abort, Api


class App():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = 'yandexlyceum_secret_key'
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
    
    def run(self):
        self.app.run(host='127.0.0.1', port=8000)

    def activate_route(self):
        @self.login_manager.user_loader
        def load_user(user_id):
            db_sess = db_session.create_session()
            return db_sess.query(User).get(user_id)

        @self.app.route('/')
        def index():
            return render_template("index.html", title="Главная страница")

        @self.app.route('/songs')
        def songs():
            db_sess = db_session.create_session()
            songs = db_sess.query(Song).all()
            songs = sorted(songs, key=lambda x: x.searches, reverse=True)
            return render_template("songs.html", title="Рейтинг страниц", songs=songs)

        @self.app.route('/authors')
        def authors():
            db_sess = db_session.create_session()
            authors = db_sess.query(Author).all()
            authors = sorted(authors, key=lambda x: x.searches, reverse=True)
            return render_template("authors.html", title="Рейтинг авторов", authors=authors)

        @self.app.route('/history')
        def history():
            db_sess = db_session.create_session()
            searches_id = current_user.searches_id.strip().split()
            searches_id = list(map(int, searches_id))
            searches = db_sess.query(Search).filter(Search.id.in_(searches_id)).all()
            searches = sorted(searches, key=lambda x: x.creation_data, reverse=True)
            return render_template('history.html', title='История', searches=searches)


        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            form = LoginForm()
            if form.validate_on_submit():
                db_session.global_init("db/music.db")
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(
                    User.name == form.name.data).first()
                if user and user.check_password(form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    return redirect('/')
                return render_template('login.html', form=form, title='Авторизация',
                                    message='Неправильный логин или пароль')
            return render_template('login.html', form=form, title='Авторизация')

        @self.app.route('/logout')
        @login_required
        def logout():
            logout_user()
            return redirect('/')

        


if __name__ == '__main__':
    app = App()
    app.activate_route()
    app.run()
