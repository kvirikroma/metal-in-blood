from typing import List

from . import database
from repositories.tables import Image


def add_image(image: Image) -> Image:
    database.session.add(image)
    database.session.commit()
    return image


def delete_image(image: Image) -> None:
    database.session.delete(image)
    database.session.commit()
    pass


def get_image_by_id(image_id: str) -> Image:
    return database.session.query(Image).filter(Image.id == image_id).first()


def delete_image_by_id(image_id: str) -> None:
    database.session.query(Image).filter(Image.id == image_id).delete()
    database.session.commit()


def get_user_images(user_id: str, page: int, page_size: int) -> List[Image]:
    return database.session.query(Image).\
        filter(Image.author == user_id).\
        order_by(Image.upload_time.desc()).\
        limit(page_size).offset(page * page_size).\
        all()


def get_user_images_count(user_id: str) -> int:
    return database.session.query(Image).filter(Image.author == user_id).count()
