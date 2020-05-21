from . import database
from models.tables import User


def get_user(login: str):
    return database.session.query(User).filter(User.login == login).first()


def get_user_by_id(user_id: str):
    return database.session.query(User).filter(User.id == user_id).first()


def add_user(login: str, password: str):
    new_user = User()
    new_user.login = login
    new_user.password_hash = password
    database.session.add(new_user)
    database.session.commit()
    return new_user


def delete_user(user: User):
    database.session.delete(user)
    database.session.commit()
