from . import database
from models.tables import NewsPost
from sqlalchemy.sql.operators import or_
from typing import List


def add_post(post: NewsPost) -> NewsPost:
    database.session.add(post)
    database.session.commit()
    return post


def delete_post(post: NewsPost) -> None:
    database.session.delete(post)
    database.session.commit()


def find_posts_by_author(author: str, page: int, page_size: int) -> List[NewsPost]:
    return database.session.query(NewsPost).\
        filter(NewsPost.author == author).order_by(NewsPost.date.desc()).\
        limit(page_size).offset(page * page_size).\
        all()


def search_posts(text_to_search: str, page: int, page_size: int) -> List[NewsPost]:
    text_to_search = "%{}%".format(text_to_search)
    return database.session.query(NewsPost).filter(or_(
                NewsPost.title.like(text_to_search),
                NewsPost.body.like(text_to_search)
        )).order_by(NewsPost.date.desc()).limit(page_size).offset(page * page_size).all()


def get_newest_posts(page: int, page_size: int) -> List[NewsPost]:
    return database.session.query(NewsPost).order_by(NewsPost.date.desc()).\
        limit(page_size).offset(page * page_size).all()


def get_post_by_id(post_id: str) -> NewsPost:
    return database.session.query(NewsPost).filter(NewsPost.id == post_id).first()
