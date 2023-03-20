import datetime
import sqlalchemy
import sys
import os

from sqlalchemy import orm
from . import db_session
from .towns import Towns


def fill_database():
    with open(os.path.join('db', 'towns.txt'), encoding='utf-8') as f:
        lines = list(map(lambda x: x.strip().split(';'), f.readlines()))
    if not lines:
        raise IOError
    towns, town_api_request_strings = zip(*lines)
    db_sess = db_session.create_session()
    for town_name, api_request_string in zip(towns, town_api_request_strings):
        town = Towns(
            town_name=town_name,
            api_request_string=api_request_string
        )
        db_sess.add(town)
    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init("db/town_guesser.sqlite")
    fill_database()
    db_sess = db_session.create_session()
    towns = db_sess.query(Towns)
    print(towns)