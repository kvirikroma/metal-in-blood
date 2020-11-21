from . import database
from repositories.tables import User


def add_user(user: User) -> User:
    database.session.add(user)
    database.session.commit()
    return user


def delete_user(user: User) -> None:
    database.session.delete(user)
    database.session.commit()


def search_user(login: str) -> User:
    login = "%{}%".format(login)
    return database.session.query(User).filter(User.login.ilike(login)).first()


def get_user_by_email(email: str) -> User:
    return database.session.query(User).filter(User.email == email).first()


def get_user_by_login(login: str) -> User:
    return database.session.query(User).filter(User.login == login).first()


def get_user_by_id(user_id: str) -> User:
    return database.session.query(User).filter(User.id == user_id).first()
