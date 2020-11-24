from typing import List
from math import ceil

from flask import abort

from repositories import tip_repository, user_repository
from repositories.tables import Tip
from . import default_page_size, check_uuid


def prepare_tips_list(tips: List[Tip]):
    for tip in tips:
        tip.tip_id = tip.id
    return tips


def get_tips(page: int):
    pages_count = tips_pages_count()
    if page <= pages_count:
        tips = prepare_tips_list(tip_repository.get_tips(page, default_page_size))
    else:
        tips = []
    return {
        "tips": tips,
        "pages_count": pages_count
    }


def tips_pages_count() -> int:
    return ceil(tip_repository.get_tips_count() / default_page_size)


def search_tips(page: int, text_to_search: str):
    return {"tips": prepare_tips_list(
        tip_repository.search_tips(text_to_search, page, default_page_size)
    )}


def add_tip(user_id: str, title: str, body: str, picture: str, **kwargs) -> Tip:
    user = user_repository.get_user_by_id(user_id)
    if not user or not (user.admin or user.change_tips):
        abort(403, "You don't have a permission to add tips")
    tip = Tip()
    tip.title = title
    tip.body = body
    tip.picture = picture
    return tip_repository.add_tip(tip)


def delete_tip(user_id: str, tip_id: str) -> None:
    check_uuid(tip_id)
    user = user_repository.get_user_by_id(user_id)
    if not user or not (user.admin or user.change_tips):
        abort(403, "You don't have a permission to remove tips")
    tip_repository.delete_tip_by_id(tip_id)
