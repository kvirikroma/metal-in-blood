from typing import List
from datetime import datetime

from flask import abort, jsonify, make_response

from repositories import forum_repository
from models.tables import ForumThread, ForumMessage
from . import default_page_size, check_uuid


def prepare_threads_list(threads: List[ForumThread]):
    for thread in threads:
        thread.thread_id = thread.id
    return threads


def prepare_messages_list(messages: List[ForumMessage]):
    for message in messages:
        message.message_id = message.id
    return messages


def add_thread(user_id: str, title: str, body: str):
    if forum_repository.get_user_thread_by_title(user_id, title):
        abort(409, "You already have thread with this title")
    thread = ForumThread()
    thread.author = user_id
    thread.title = title
    thread.body = body
    thread.date = datetime.today()
    forum_repository.add_forum_thread(thread)


def delete_thread(user_id: str, thread_id: str):
    thread = forum_repository.get_thread_by_id(thread_id)
    if thread.author != user_id:
        abort(403, "You can delete only your own threads")
    forum_repository.delete_forum_thread(thread)


def add_message(user_id: str, related_to: str, body: str):
    if not forum_repository.get_thread_by_id(related_to):
        abort(make_response(jsonify(message="Thread does not exist"), 404))
    message = ForumMessage()
    message.date = datetime.now()
    message.body = body
    message.related_to = related_to
    message.author = user_id
    forum_repository.add_thread_message(message)


def delete_message(user_id: str, message_id: str):
    message = forum_repository.get_message_by_id(message_id)
    if message.author != user_id:
        abort(403, "You can delete only your own messages")
    forum_repository.delete_thread_message(message)


def get_threads(page: int):
    return {"threads": forum_repository.get_newest_threads_with_info(page, default_page_size)}


def search_threads(page: int, text_to_search: str):
    return {"threads": prepare_threads_list(
        forum_repository.search_threads(text_to_search, page, default_page_size)
    )}


def get_messages(page: int, thread_id: str):
    check_uuid(thread_id)
    return {"messages": prepare_messages_list(
        forum_repository.get_thread_messages(thread_id, page, default_page_size)
    )}


def search_messages(page: int, thread_id: str, text_to_search: str):
    check_uuid(thread_id)
    return {"messages": prepare_messages_list(
        forum_repository.search_messages(text_to_search, thread_id, page, default_page_size)
    )}
