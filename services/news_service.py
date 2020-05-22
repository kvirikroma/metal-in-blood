from datetime import datetime
from typing import List

from repositories import news_repository
from models.tables import NewsPost
from . import default_page_size


def prepare_posts_list(posts: List[NewsPost]):
    for post in posts:
        post.post_id = post.id
    return posts


def get_newest_posts(page: int):
    return {"posts": prepare_posts_list(
        news_repository.get_newest_posts(page, default_page_size)
    )}


def search_posts(page: int, text_to_search: str):
    return {"posts": prepare_posts_list(
        news_repository.search_posts(text_to_search, page, default_page_size)
    )}


def add_post(user_id: str, title: str, body: str, picture: str):
    pass


def delete_post(user_id: str, post_id: str):
    pass
