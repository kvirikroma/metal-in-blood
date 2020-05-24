import bcrypt

from flask import abort, make_response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

from repositories import user_repository
from models.tables import User


def check_password(password: str):
    letters = "abcdefghijklmnopqrstuvwxyz"
    lower = False
    upper = False
    digit = False
    for letter in password:
        check = False
        if letters.find(letter) != -1:
            check = True
            lower = True
        if letters.upper().find(letter) != -1:
            check = True
            upper = True
        if "-.?!@=".find(letter) != -1:
            check = True
        if letter.isdigit():
            check = True
            digit = True
        if not check:
            abort(make_response(jsonify(message="Password cannot contain symbols like this: '" + letter + "'"), 400))
    if not lower:
        abort(make_response(jsonify(message="Password must contain at least one lowercase letter"), 400))
    if not upper:
        abort(make_response(jsonify(message="Password must contain at least one uppercase letter"), 400))
    if not digit:
        abort(make_response(jsonify(message="Password must contain at least one digit"), 400))


def register_user(email: str, login: str, password: str):
    if user_repository.get_user_by_login(login) is not None:
        abort(409, "User with this login already exists")
    if user_repository.get_user_by_email(email) is not None:
        abort(409, "User with this email already exists")
    check_password(password)
    user = User()
    user.email = email
    user.login = login
    user.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
    user_repository.add_user(user)


def get_token(login: str, password: str):
    user = user_repository.get_user_by_login(login)
    if not user:
        abort(404, "User not found")
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        abort(401, "Invalid credentials given")
    return {
        'access_token': create_access_token(identity=user.id),
        'refresh_token': create_refresh_token(identity=user.id),
        "user_id": user.id
    }
