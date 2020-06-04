from typing import List

from repositories import compilation_repository
from models.tables import Album, YTCompilation
from . import default_page_size


def prepare_albums_list(albums: List[Album]):
    for album in albums:
        album.album_id = album.id
        album.title = album.album_name
    return albums


def prepare_compilations_list(compilations: List[YTCompilation]):
    for compilation in compilations:
        compilation.compilation_id = compilation.id
    return compilations


def get_albums(page: int):
    return {"albums": prepare_albums_list(
        compilation_repository.get_albums(page, default_page_size)
    )}


def search_albums(page: int, text_to_search: str):
    return {"albums": prepare_albums_list(
        compilation_repository.search_albums(text_to_search, page, default_page_size)
    )}


def get_compilations(page: int):
    return {"compilations": prepare_compilations_list(
        compilation_repository.get_compilations(page, default_page_size)
    )}


def search_compilations(page: int, text_to_search: str):
    return {"compilations": prepare_compilations_list(
        compilation_repository.search_compilations(text_to_search, page, default_page_size)
    )}
