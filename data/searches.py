import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import datetime


class Search(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'searhes'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    song_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('songs.id'))
    user = orm.relation('User')
    song = orm.relation('Song')
    creation_data = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)
