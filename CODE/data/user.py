import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    date = sqlalchemy.Column(sqlalchemy.DATE, nullable=True, default=0)

    news_first_choice = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="Europe/London")
    news_second_choice = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="America/Los_Angeles")
    news_third_choice = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="Asia/Hong_Kong")
