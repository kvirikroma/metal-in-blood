from typing import List
from datetime import datetime
from math import ceil

from flask import abort

from repositories import forum_repository, user_repository, ForumThread, ForumMessage
from . import default_page_size, check_uuid


def prepare_threads_list(threads: List[ForumThread or dict]):
    for thread in threads:
        if isinstance(thread, dict):
            if not thread.get('thread_id'):
                thread['thread_id'] = thread['id']
        else:
            thread.thread_id = thread.id
    return threads


def prepare_messages_list(messages: List[ForumMessage or dict]):
    for message in messages:
        if isinstance(message, dict):
            message['message_id'] = message['id']
        else:
            message.message_id = message.id
    return messages


def add_thread(user_id: str, title: str, body: str, **kwargs):
    if forum_repository.get_user_thread_by_title(user_id, title):
        abort(409, "You already have thread with this title")
    thread = ForumThread()
    thread.author = user_id
    thread.title = title
    thread.body = body
    thread.date = datetime.today()
    forum_repository.add_forum_thread(thread)
    thread.thread_id = thread.id
    thread.messages_count = 0
    thread.users_count = 0
    return thread


def delete_thread(user_id: str, thread_id: str):
    check_uuid(thread_id)
    thread = forum_repository.get_thread_by_id(thread_id)
    if not thread:
        abort(404, "Thread does not exist")
    if thread.author != user_id:
        user_that_removes = user_repository.get_user_by_id(user_id)
        if not user_that_removes or not user_that_removes.admin:
            abort(403, "You can delete only your own threads")
    forum_repository.delete_forum_thread(thread)


def add_message(user_id: str, related_to: str, body: str, **kwargs):
    check_uuid(related_to)
    if not forum_repository.get_thread_by_id(related_to):
        abort(404, "Thread does not exist")
    message = ForumMessage()
    message.date = datetime.now()
    message.body = body
    message.related_to = related_to
    message.author = user_id
    forum_repository.add_thread_message(message)


def delete_message(user_id: str, message_id: str):
    check_uuid(message_id)
    message = forum_repository.get_message_by_id(message_id)
    if not message:
        abort(404, "Message does not exist")
    if message.author != user_id:
        user_that_removes = user_repository.get_user_by_id(user_id)
        if not user_that_removes or not user_that_removes.admin:
            abort(403, "You can delete only your own messages")
    forum_repository.delete_thread_message(message)


def threads_pages_count():
    return ceil(forum_repository.get_threads_count() / default_page_size)


def thread_messages_pages_count(thread_id: str):
    return ceil(forum_repository.get_thread_messages_count(thread_id) / default_page_size)


def get_threads(page: int):
    pages_count = threads_pages_count()
    if page <= pages_count:
        threads = prepare_threads_list(forum_repository.get_newest_threads_with_info(page, default_page_size))
    else:
        threads = []
    return {
        "threads": threads,
        "pages_count": pages_count
    }


def search_threads(page: int, text_to_search: str):
    return {"threads": prepare_threads_list(
        forum_repository.search_threads(text_to_search, page, default_page_size)
    )}


def get_messages(page: int, thread_id: str):
    check_uuid(thread_id)
    pages_count = thread_messages_pages_count(thread_id)
    if page <= pages_count:
        messages = prepare_messages_list(forum_repository.get_thread_messages(thread_id, page, default_page_size))
    else:
        messages = []
    if not messages and not forum_repository.get_thread_by_id(thread_id):
        abort(404, "Thread does not exist")
    return {"messages": messages}


def search_messages(page: int, thread_id: str, text_to_search: str):
    check_uuid(thread_id)
    return {"messages": prepare_messages_list(
        forum_repository.search_messages(text_to_search, thread_id, page, default_page_size)
    )}
