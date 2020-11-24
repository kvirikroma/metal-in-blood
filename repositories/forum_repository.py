from typing import List, Dict
from os import path

from sqlalchemy.sql.operators import or_
from sqlalchemy import func, distinct
from flask import current_app

from repositories.tables import ForumThread, ForumMessage, User
from . import database, parse_raw_join_result


def add_forum_thread(thread: ForumThread) -> ForumThread:
    database.session.add(thread)
    database.session.commit()
    return thread


def delete_forum_thread(thread: ForumThread) -> None:
    database.session.delete(thread)
    database.session.commit()


def get_threads_count() -> int:
    return database.session.query(ForumThread).count()


def search_threads(text_to_search: str, page: int, page_size: int) -> List[Dict]:
    text_to_search = "%{}%".format(text_to_search)

    count_request = database.session.query(
        func.count("*"),
        func.count(distinct(ForumMessage.author)),
        ForumMessage.related_to
    ).group_by(ForumMessage.related_to).subquery()

    raw_result = database.session.query(ForumThread, User.login, count_request).\
        outerjoin(count_request, count_request.c.related_to == ForumThread.id).\
        filter(User.id == ForumThread.author).\
        filter(or_(
                ForumThread.title.ilike(text_to_search),
                ForumThread.body.ilike(text_to_search)
        )).order_by(ForumThread.date.desc()).limit(page_size).offset(page * page_size).all()

    result = []
    for thread, author, messages, people, thread_id in raw_result:
        thread = thread.__dict__
        thread['author'], thread['messages_count'], thread['users_count'] = (
            author,
            messages if messages else 0,
            people if people else 0
        )
        result.append(thread)

    return result


def get_newest_threads(page: int, page_size: int) -> List[Dict]:
    result = database.session.query(ForumThread, User.login).\
        filter(User.id == ForumThread.author).\
        order_by(ForumThread.date.desc()).\
        limit(page_size).offset(page * page_size).all()
    return parse_raw_join_result(result)


def get_newest_threads_with_info(page: int, page_size: int) -> List[Dict]:
    database.session.rollback()
    with open(path.join(current_app.root_path, "sql/forum_data.sql"), 'r') as query_file:
        query = query_file.read().format(page_size, page * page_size)
    raw_result = database.engine.connect().execute(query)
    return [
        {
            ('thread_id' if column == 'id' else column): value for column, value in row_proxy.items()
        } for row_proxy in raw_result
    ]


def get_user_threads(user_id: str, page: int, page_size: int) -> List[ForumThread]:
    return database.session.query(ForumThread).\
        filter(ForumThread.author == user_id).\
        order_by(ForumThread.date.desc()).\
        limit(page_size).offset(page * page_size).all()


def get_user_thread_by_title(user_id: str, title: str) -> ForumThread:
    return database.session.query(ForumThread).\
        filter(ForumThread.author == user_id).\
        filter(ForumThread.title == title).first()


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


def get_raw_thread_messages(thread_id: str, page: int, page_size: int) -> List[ForumMessage]:
    return database.session.query(ForumMessage).\
        filter(ForumMessage.related_to == thread_id).order_by(ForumMessage.date.asc()).\
        limit(page_size).offset(page * page_size).all()


def get_thread_messages(thread_id: str, page: int, page_size: int) -> List[Dict]:
    result = database.session.query(ForumMessage, User.login).\
        filter(User.id == ForumMessage.author).\
        filter(ForumMessage.related_to == thread_id).order_by(ForumMessage.date.asc()).\
        limit(page_size).offset(page * page_size).all()
    return parse_raw_join_result(result)


def get_thread_messages_count(thread_id: str) -> int:
    return database.session.query(ForumMessage).filter(ForumMessage.related_to == thread_id).count()


def get_message_by_id(message_id: str) -> ForumMessage:
    return database.session.query(ForumMessage).\
        filter(ForumMessage.id == message_id).first()


def search_messages(text_to_search: str, thread_id: str, page: int, page_size: int) -> List[Dict]:
    text_to_search = "%{}%".format(text_to_search)
    result = database.session.query(ForumMessage, User.login).\
        filter(User.id == ForumMessage.author).\
        filter(ForumMessage.related_to == thread_id).\
        filter(ForumMessage.body.ilike(text_to_search)).\
        order_by(ForumMessage.date.desc()).limit(page_size).offset(page * page_size).all()
    return parse_raw_join_result(result)
