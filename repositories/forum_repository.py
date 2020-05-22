from . import database
from models.tables import ForumThread, ForumMessage
from sqlalchemy.sql.operators import or_
from typing import List


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


def get_user_threads(user_id: str, page: int, page_size: int) -> List[ForumThread]:
    return database.session.query(ForumThread).\
        filter(ForumThread.author == user_id).order_by(ForumThread.date.desc()).\
        limit(page_size).offset(page * page_size).all()


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
