from flask import abort
from flask_jwt_extended import create_access_token, create_refresh_token

from repositories import user_repository
from models.tables import User


def register_user(email: str, login: str, password: str):
    pass


def get_token(login: str, password: str = None):
    pass
