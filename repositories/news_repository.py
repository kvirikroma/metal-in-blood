from typing import List, Dict

from sqlalchemy.sql.operators import or_

from . import database, parse_raw_join_result
from repositories.tables import NewsPost, User


def add_post(post: NewsPost) -> NewsPost:
    database.session.add(post)
    database.session.commit()
    return post


def delete_post(post: NewsPost) -> None:
    database.session.delete(post)
    database.session.commit()


def find_posts_by_author(author: str, page: int, page_size: int) -> List[Dict]:
    result = database.session.query(NewsPost, User.login).\
        filter(User.id == NewsPost.author).\
        filter(NewsPost.author == author).order_by(NewsPost.date.desc()).\
        limit(page_size).offset(page * page_size).\
        all()
    return parse_raw_join_result(result)


def search_posts(text_to_search: str, page: int, page_size: int) -> List[Dict]:
    text_to_search = "%{}%".format(text_to_search)
    result = database.session.query(NewsPost, User).\
        filter(User.id == NewsPost.author).\
        filter(or_(
                NewsPost.title.ilike(text_to_search),
                NewsPost.body.ilike(text_to_search)
        )).order_by(NewsPost.date.desc()).limit(page_size).offset(page * page_size).all()
    return parse_raw_join_result(result)


def get_newest_posts(page: int, page_size: int) -> List[Dict]:
    result = database.session.query(NewsPost, User.login).\
        filter(User.id == NewsPost.author).\
        order_by(NewsPost.date.desc()).\
        limit(page_size).offset(page * page_size).all()
    return parse_raw_join_result(result)


def get_post_by_id(post_id: str) -> NewsPost:
    return database.session.query(NewsPost).filter(NewsPost.id == post_id).first()
