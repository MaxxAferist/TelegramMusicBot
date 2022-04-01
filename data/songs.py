from email.policy import default
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Song(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'songs'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    artist = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('authors.id'))
    url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    searches = sqlalchemy.Column(sqlalchemy.Integer)
