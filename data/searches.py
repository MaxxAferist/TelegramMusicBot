import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Search(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'searhes'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    search = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    title = sqlalchemy.Column(sqlalchemy.String)
    artist = sqlalchemy.Column(sqlalchemy.String)
    lyrics = sqlalchemy.Column(sqlalchemy.String)
