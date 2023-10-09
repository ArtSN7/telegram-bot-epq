import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)