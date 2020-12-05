from datetime import datetime
from typing import List, Dict
from math import ceil

from flask import abort

from repositories import news_repository, user_repository, NewsPost
from . import default_page_size, check_uuid


def prepare_posts_list(posts: List[NewsPost or Dict]) -> List[NewsPost or Dict]:
    for post in posts:
        if isinstance(post, dict):
            if not post.get('post_id'):
                post['post_id'] = post['id']
        else:
            post.post_id = post.id
    return posts


def get_newest_posts(page: int):
    pages_count = newest_posts_pages_count()
    if page <= pages_count:
        posts = prepare_posts_list(news_repository.get_newest_posts(page, default_page_size))
    else:
        posts = []
    return {
        "posts": posts,
        "pages_count": pages_count
    }


def newest_posts_pages_count():
    return ceil(news_repository.get_posts_count() / default_page_size)


def search_posts(page: int, text_to_search: str):
    return {"posts": prepare_posts_list(
        news_repository.search_posts(text_to_search, page, default_page_size)
    )}


def add_post(user_id: str, title: str, body: str, picture: str = None, **kwargs):
    author = user_repository.get_user_by_id(user_id)
    if not author or (not author.change_news and not author.admin):
        abort(403, "You don't have permission to add posts here")
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
        abort(404, "Post does not exist")
    if post.author != user_id:
        abort(403, "You can delete only your own posts")
    news_repository.delete_post(post)
