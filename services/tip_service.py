from typing import List

from repositories import tip_repository
from models.tables import Tip
from . import default_page_size


def prepare_tips_list(tips: List[Tip]):
    for tip in tips:
        tip.tip_id = tip.id
    return tips


def get_tips(page: int):
    return {"tips": prepare_tips_list(
        tip_repository.get_tips(page, default_page_size)
    )}


def search_tips(page: int, text_to_search: str):
    return {"tips": prepare_tips_list(
        tip_repository.search_tips(text_to_search, page, default_page_size)
    )}
