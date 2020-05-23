from typing import List

from repositories import forum_repository
from models.tables import ForumThread, ForumMessage
from . import default_page_size


def prepare_threads_list(threads: List[ForumThread]):
    for thread in threads:
        thread.thread_id = thread.id
    return threads


def prepare_messages_list(messages: List[ForumMessage]):
    for message in messages:
        message.message_id = message.id
    return messages


def add_thread(user_id: str, title: str, body: str):
    pass


def delete_thread(user_id: str, thread_id: str):
    pass


def add_message(user_id: str, related_to: str, body: str):
    pass


def delete_message(user_id: str, message_id: str):
    pass


def get_threads(page: int):
    pass


def search_threads(page: int, text_to_search: str):
    pass


def get_messages(page: int, thread_id: str):
    pass


def search_messages(page: int, thread_id: str, text_to_search: str):
    pass
