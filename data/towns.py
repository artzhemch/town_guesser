import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Towns(SqlAlchemyBase):
    __tablename__ = 'towns'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    town_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    api_request_string = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adding_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    def __repr__(self):
        return f'<Towns> Town_name = {self.town_name}, Api_request = {self.api_request_string}'
