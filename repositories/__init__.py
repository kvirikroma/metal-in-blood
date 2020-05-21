from injector import inject
from flask_sqlalchemy import SQLAlchemy


class DbGetter:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db


database = DbGetter().db
