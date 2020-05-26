from injector import inject, Injector
from flask_sqlalchemy import SQLAlchemy


class DbGetter:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db


database = Injector().get(DbGetter).db


def parse_raw_join_result(result: list):
    for i in range(len(result)):
        name = result[i][1]
        result[i] = result[i][0].__dict__
        result[i]['author'] = name
    return result
