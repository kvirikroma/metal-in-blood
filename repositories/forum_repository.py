from typing import List, Dict
from os import path

from sqlalchemy.sql.operators import or_
from flask import current_app, Flask

from models.tables import ForumThread, ForumMessage
from . import database

current_app: Flask


def add_forum_thread(thread: ForumThread) -> ForumThread:
    database.session.add(thread)
    database.session.commit()
    return thread


def delete_forum_thread(thread: ForumThread) -> None:
    database.session.delete(thread)
    database.session.commit()


def search_threads(text_to_search: str, page: int, page_size: int) -> List[ForumThread]:
    text_to_search = "%{}%".format(text_to_search)
    return database.session.query(ForumThread).filter(or_(
                ForumThread.title.like(text_to_search),
                ForumThread.body.like(text_to_search)
        )).order_by(ForumThread.date.desc()).limit(page_size).offset(page * page_size).all()


def get_newest_threads(page: int, page_size: int) -> List[ForumThread]:
    return database.session.query(ForumThread).order_by(ForumThread.date.desc()).\
        limit(page_size).offset(page * page_size).all()


def get_newest_threads_with_info(page: int, page_size: int) -> List[Dict]:
    with open(path.join(current_app.root_path, "sql/forum_data.sql"), 'r') as query_file:
        query = query_file.read().format(page_size, page * page_size)
    raw_result = database.engine.connect().execute(query)
    return [{column: value for column, value in row_proxy.items()} for row_proxy in raw_result]


def get_user_threads(user_id: str, page: int, page_size: int) -> List[ForumThread]:
    return database.session.query(ForumThread).\
        filter(ForumThread.author == user_id).order_by(ForumThread.date.desc()).\
        limit(page_size).offset(page * page_size).all()


def get_user_thread_by_title(user_id: str, title: str) -> ForumThread:
    return database.session.query(ForumThread).\
        filter(ForumThread.author == user_id).\
        friler(ForumThread.title == title).first()


def get_thread_by_id(thread_id: str) -> ForumThread:
    return database.session.query(ForumThread).\
        filter(ForumThread.id == thread_id).first()


def add_thread_message(message: ForumMessage) -> ForumMessage:
    database.session.add(message)
    database.session.commit()
    return message


def delete_thread_message(message: ForumMessage) -> None:
    database.session.delete(message)
    database.session.commit()


def get_thread_messages(thread_id: str, page: int, page_size: int) -> List[ForumMessage]:
    return database.session.query(ForumMessage).\
        filter(ForumMessage.related_to == thread_id).order_by(ForumMessage.date.asc()).\
        limit(page_size).offset(page * page_size).all()


def get_message_by_id(message_id: str) -> ForumMessage:
    return database.session.query(ForumMessage).\
        filter(ForumMessage.id == message_id).first()


def search_messages(text_to_search: str, thread_id: str, page: int, page_size: int) -> List[ForumThread]:
    text_to_search = "%{}%".format(text_to_search)
    return database.session.query(ForumMessage).filter(or_(
                ForumMessage.title.like(text_to_search),
                ForumMessage.body.like(text_to_search)
        )).filter(ForumMessage.related_to == thread_id).\
        order_by(ForumMessage.date.desc()).limit(page_size).offset(page * page_size).all()
