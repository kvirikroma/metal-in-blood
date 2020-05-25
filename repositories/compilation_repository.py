from typing import List

from sqlalchemy.sql.operators import or_

from . import database
from models.tables import YTCompilation, Album


def add_album(album: Album) -> Album:
    database.session.add(album)
    database.session.commit()
    return album


def delete_album(album: Album) -> None:
    database.session.delete(album)
    database.session.commit()


def search_albums(text_to_search: str, page: int, page_size: int) -> List[Album]:
    text_to_search = "%{}%".format(text_to_search)
    return database.session.query(Album).filter(or_(
                Album.author.ilike(text_to_search),
                Album.album_name.ilike(text_to_search)
        )).limit(page_size).offset(page * page_size).all()


def get_albums(page: int, page_size: int) -> List[Album]:
    return database.session.query(Album).limit(page_size).offset(page * page_size).all()


def add_compilation(compilation: YTCompilation) -> YTCompilation:
    database.session.add(compilation)
    database.session.commit()
    return compilation


def delete_compilation(compilation: YTCompilation) -> None:
    database.session.delete(compilation)
    database.session.commit()


def get_compilations(page: int, page_size: int) -> List[YTCompilation]:
    return database.session.query(YTCompilation).limit(page_size).offset(page * page_size).all()


def search_compilations(text_to_search: str, page: int, page_size: int) -> List[YTCompilation]:
    text_to_search = "%{}%".format(text_to_search)
    return database.session.query(YTCompilation).filter(or_(
                YTCompilation.channel.ilike(text_to_search),
                YTCompilation.video_name.ilike(text_to_search)
        )).limit(page_size).offset(page * page_size).all()
