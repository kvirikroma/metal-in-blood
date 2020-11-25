from typing import List
from os import path, makedirs, removedirs, remove, listdir

from flask import current_app
from werkzeug.datastructures import FileStorage

from . import database
from repositories.tables import Image


IMAGE_DEFAULT_NAME = "image"


def common_image_path():
    return path.join(current_app.config["UPLOAD_FOLDER"], "images")


def path_from_id(image_id: str) -> str:
    image_path_inner = str.join('/', list(image_id.replace('-', '')))
    return path.join(common_image_path(), image_path_inner)


def full_path_by_id(image_id: str, image_name: str) -> str:
    save_path = path_from_id(image_id)
    image_full_name = image_name.split('.')
    image_new_name = IMAGE_DEFAULT_NAME
    if len(image_full_name) > 1:
        image_new_name += f".{image_full_name[-1]}"
    return path.join(save_path, image_new_name)


def get_image_filename(image_id: str):
    image_path = path_from_id(image_id)
    if path.exists(image_path):
        for file in listdir(image_path):
            if file.startswith(IMAGE_DEFAULT_NAME):
                return file


def remove_image_file_by_id(image_id: str):
    image_path = path_from_id(image_id)
    if path.exists(image_path):
        for file in listdir(image_path):
            remove(path.join(image_path, file))
        removedirs(image_path)
        makedirs(common_image_path(), exist_ok=True)


def add_image(image: Image, image_file: FileStorage) -> Image:
    image_path = path_from_id(image.id)
    makedirs(image_path)
    image_file.save(full_path_by_id(image.id, image_file.filename))
    database.session.add(image)
    database.session.commit()
    return image


def delete_image(image: Image) -> None:
    remove_image_file_by_id(image.id)
    database.session.delete(image)
    database.session.commit()


def get_image_by_id(image_id: str) -> Image:
    return database.session.query(Image).filter(Image.id == image_id).first()


def delete_image_by_id(image_id: str) -> None:
    remove_image_file_by_id(image_id)
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
