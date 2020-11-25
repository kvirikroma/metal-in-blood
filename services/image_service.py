from datetime import datetime
from typing import List, Dict
from math import ceil
from uuid import uuid4

from flask import abort, Response, send_from_directory
from werkzeug.datastructures import FileStorage

from repositories import image_repository, user_repository
from repositories.tables import Image
from . import default_page_size, check_uuid


def prepare_images_list(images: List[Image or dict]):
    for image in images:
        if isinstance(image, dict):
            image['image_id'] = image['id']
        else:
            image.image_id = image.id
    return images


def save_image(user_id: str, image_file: FileStorage) -> dict:
    image = Image()
    image.author = user_id
    image.upload_time = datetime.now()
    image.id = str(uuid4())

    result = image_repository.add_image(image, image_file).__dict__
    result["image_id"] = image.id
    return result


def get_image(image_id: str) -> Response:
    check_uuid(image_id)
    if not image_repository.get_image_by_id(image_id):
        abort(404, "Image not found")
    return send_from_directory(
        image_repository.path_from_id(image_id),
        image_repository.get_image_filename(image_id),
        as_attachment=True
    )


def delete_image(user_id: str, image_id: str) -> None:
    check_uuid(image_id)
    image = image_repository.get_image_by_id(image_id)
    if not image:
        abort(404, "Image not found")
    if image.author != user_id:
        user = user_repository.get_user_by_id(user_id)
        if not user or not user.admin:
            abort(403, "You can not remove images of other users")
        if image.user.admin and not user.change_admins:
            abort(403, "You don't have permission to remove pictures of admins")
    image_repository.delete_image(image)


def images_pages_count(user_id: str):
    return ceil(image_repository.get_user_images_count(user_id) / default_page_size)


def get_all_images(user_id: str, page: int) -> Dict[str, List[Image]]:
    pages_count = images_pages_count(user_id)
    if page <= pages_count:
        images = prepare_images_list(image_repository.get_user_images(user_id, page, default_page_size))
    else:
        images = []
    return {
        "images": images,
        "pages_count": pages_count
    }
