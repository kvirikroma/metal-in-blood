from datetime import datetime
from typing import List

from flask import abort, jsonify, make_response

from repositories import news_repository
from models.tables import NewsPost
from . import default_page_size, check_uuid


def prepare_posts_list(posts: List[NewsPost]):
    for post in posts:
        if isinstance(post, dict):
            post['post_id'] = post['id']
        else:
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


def add_post(user_id: str, title: str, body: str, picture: str = None):
    post = NewsPost()
    post.author = user_id
    post.date = datetime.today()
    post.title = title
    post.body = body
    post.picture = picture
    news_repository.add_post(post)


def delete_post(user_id: str, post_id: str):
    check_uuid(post_id)
    post = news_repository.get_post_by_id(post_id)
    if not post:
        abort(make_response(jsonify(message="Post does not exist"), 404))
    if post.author != user_id:
        abort(403, "You can delete only your own posts")
    news_repository.delete_post(post)
