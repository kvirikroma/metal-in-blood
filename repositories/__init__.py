from injector import inject, Injector
from flask_sqlalchemy import SQLAlchemy


class DbGetter:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db


database = Injector().get(DbGetter).db
