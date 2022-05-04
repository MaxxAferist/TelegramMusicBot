import flask
from . import db_session
from flask import jsonify, request
from .users import User
from .songs import Song
from .authors import Author
from .searches import Search


blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)

# Найти пользователя по id


@blueprint.route('/api/user/get/<int:id>', methods=['GET'])
def get_user(id):
    sess = db_session.create_session()
    user = sess.query(User).filter(User.id == id).first()
    if not user:
        return jsonify({'Error': 'Not found'})
    return jsonify({'user': user.to_dict(only=('id', 'name', 'searches_id', 'points'))})


# Добавляем запрос к музыке
@blueprint.route('/api/song/add_searches', methods=['POST'])
def song_add_searches():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    title = request.json.get("title")
    artist = request.json.get("artist")
    url = request.json.get("url")
    db_sess = db_session.create_session()
    song_db = db_sess.query(Song).filter(
        (Song.title == title) & (Song.artist == artist)).first()
    if song_db:
        song_db.searches += 1
    else:
        song_db = Song(
            title=title,
            artist=artist,
            url=url,
            searches=1
        )
        db_sess.add(song_db)
        db_sess.commit()
    return jsonify({"OK": "Success", "song_id": song_db.id})


# Добавляем запрос к автору
@blueprint.route('/api/authors/add_searhes', methods=['POST'])
def author_add_searches():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    artist = request.json.get('artist')
    db_sess = db_session.create_session()
    author_db = db_sess.query(Author).filter(
        Author.name == artist).first()
    if author_db:
        author_db.searches += 1
    else:
        author_db = Author(
            name=artist,
            searches=1
        )
        db_sess.add(author_db)
        db_sess.commit()
    return jsonify({'OK': "Success"})


# Создаем запрос
@blueprint.route('/api/searches/add', methods=['POST'])
def add_search():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    user_id = request.json.get('user_id')
    song_id = request.json.get('song_id')
    success = request.json.get('success')

    db_sess = db_session.create_session()
    search = Search(
        user_id=user_id,
        song_id=song_id
    )
    db_sess.add(search)
    if success:
        user = db_sess.query(User).filter(User.id == user_id).first()
        user.searches_id = str(user.searches_id) + ' ' + str(search.id)
    db_sess.commit()
    return jsonify({'OK': "Success"})


# Регистрация - имя пользователя
@blueprint.route('/api/register/name', methods=['POST'])
def register_name():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    name = request.json.get('name')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == name).first()
    if user:
        message = "Имя занято. Попробуйте другое!"
        return jsonify({'message': message})
    return jsonify({'message': "success"})


# Регистрация - заносим пользователя в бд
@blueprint.route('/api/register/user', methods=['POST'])
def register_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    name = request.json.get('name')
    password = request.json.get('password')

    db_sess = db_session.create_session()
    user = User()
    user.name = name
    user.set_password(password)
    user.searches_id = ''
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'OK': 'Success', 'user_id': user.id})


# Вход - проверка имени
@blueprint.route('/api/login/name', methods=['POST'])
def login_name():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    name = request.json.get('name')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == name).first()
    if not user:
        return jsonify({"message": "Такого пользователя не существует"})
    return jsonify({"message": "success"})


# Вход - проверка пароля
@blueprint.route('/api/login/password', methods=['POST'])
def login_password():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    login_name = request.json.get('login_name')
    password = request.json.get('password')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        User.name == login_name).first()
    if user.check_password(password):
        return jsonify({'result': True, 'user_id': user.id})
    return jsonify({'result': False})


# Игра - зачисление очков пользователя
@blueprint.route('/api/game/enrollment_points', methods=['POST'])
def game_enrollment_points():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    user_id = request.json.get('user_id')
    points = request.json.get('points')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        User.id == user_id).first()
    user.points = points
    db_sess.commit()
    return jsonify({'OK': 'success'})


# Игра - получение очков пользователя
@blueprint.route('/api/game/get_points/<int:id>')
def game_get_points(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        User.id == id).first()
    points = user.points
    name = user.name
    return jsonify({'name': name, 'points': points})


# Регистрация(игра) - заносим пользователя в бд
@blueprint.route('/api/game/register/user', methods=['POST'])
def game_register_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    name = request.json.get('name')
    password = request.json.get('password')
    print(name)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == name).first()
    if user:
        message = "Имя занято. Попробуйте другое!"
        return jsonify({'message': message, 'OK': False})
    user = User()
    user.name = name
    user.set_password(password)
    user.searches_id = ''
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'OK': True, 'user_id': user.id})


# Вход(игра)
@blueprint.route('/api/game/login/name', methods=['POST'])
def game_login():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    name = request.json.get('name')
    password = request.json.get('password')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == name).first()
    if not user:
        return jsonify({"message": "Такого пользователя не существует",
                        'result': False,
                        'error': 415})
    if user.check_password(password):
        return jsonify({'result': True, 'user_id': user.id})
    return jsonify({"result": False, 'error': 424})
