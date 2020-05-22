from typing import List

from repositories import compilation_repository
from models.tables import Album, YTCompilation
from . import default_page_size


def prepare_albums_list(albums: List[Album]):
    for album in albums:
        album.album_id = album.id
    return albums


def prepare_compilations_list(compilations: List[YTCompilation]):
    for compilation in compilations:
        compilation.compilation_id = compilation.id
    return compilations


def get_albums(page: int):
    pass


def search_albums(page: int, text_to_search: str):
    pass


def get_compilations(page: int):
    pass


def search_compilations(page: int, text_to_search: str):
    pass
