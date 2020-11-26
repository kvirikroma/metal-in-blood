import bcrypt
from flask import abort
from flask_jwt_extended import create_access_token, create_refresh_token

from repositories import user_repository
from repositories.tables import User
from models.user_model import user_edit_model, Language
from . import check_uuid


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
        if "-.?!@=_^:;#$%&*()+\\<>~`/\"'".find(letter) != -1:
            check = True
        if letter.isdigit():
            check = True
            digit = True
        if not check:
            abort(400, f"Password cannot contain symbols like this: '{letter}'")
    if not lower:
        abort(400, "Password must contain at least one lowercase letter")
    if not upper:
        abort(400, "Password must contain at least one uppercase letter")
    if not digit:
        abort(400, "Password must contain at least one digit")


def register_user(email: str, login: str, password: str, **kwargs):
    if user_repository.get_user_by_login(login) is not None:
        abort(409, "User with this login already exists")
    if user_repository.get_user_by_email(email) is not None:
        abort(409, "User with this email already exists")
    check_password(password)
    user = User()
    user.email = email
    user.login = login
    user.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode()
    user_repository.add_or_edit_user(user)


def get_token(login: str, password: str, **kwargs):
    user = user_repository.get_user_by_login(login)
    if not user:
        abort(404, "User not found")
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        abort(401, "Invalid credentials given")
    return {
        "access_token": create_access_token(identity=user.id),
        "refresh_token": create_refresh_token(identity=user.id),
        "user_id": user.id
    }


def get_user(user_id: str) -> dict:
    check_uuid(user_id)
    user = user_repository.get_user_by_id(user_id)
    if not user:
        abort(404, "User not found")
    result = user.__dict__
    result["user_id"] = user.id
    result["language"] = Language(user.language).name
    return result


def delete_user(own_id: str, user_id: str):
    check_uuid(user_id)
    user_that_deletes = user_repository.get_user_by_id(own_id)
    if not user_that_deletes:
        abort(401, "Deleter (user) not found")
    if own_id == user_id:
        return user_repository.delete_user(user_that_deletes)

    if not user_that_deletes.admin:
        abort(403, "Non-admins cannot remove other users")

    user = user_repository.get_user_by_id(user_id)
    if not user:
        abort(404, "User not found")
    if user.admin and not user_that_deletes.change_admins:
        abort(403, "You can not create, change or delete admins")
    user_repository.delete_user(user)


def edit_user(editor_id: str, user_id: str, **kwargs):

    def _edit_user_properties(usr: User, changes_self: bool = False, **kw_args):
        for item in kw_args:
            if item not in user_edit_model:
                abort(422, f"Cannot find key {item} in request model")
            if changes_self and (item in {"change_tips", "change_news", "change_compilations", "change_admins", "admin"}):
                if usr.change_admins:
                    if item in {"change_admins", "admin"} and not kw_args[item]:
                        abort(403, f"You can not restrict your own administration abilities")
                else:
                    abort(403, f"You can not change your own privileges")
        if "language" in kw_args:
            kw_args["language"] = Language[kw_args["language"]].value
        if kw_args.get("admin") is not None:
            if not kw_args["admin"]:
                if kw_args.get("change_admins"):
                    abort(422, f"Non-admin users can not have ability to change admins")
        if kw_args.get("change_admins"):
            kw_args["admin"] = True
        user_repository.edit_user(usr.id, kw_args)

    def _update_user(usr: User):
        result = usr.__dict__
        result.update(kwargs)
        result["user_id"] = result.get("id")
        result["language"] = Language(user.language).name
        return result

    check_uuid(user_id)
    user_that_edits = user_repository.get_user_by_id(editor_id)
    if not user_that_edits:
        abort(401, "Editor (user) not found")
    if editor_id == user_id:
        _edit_user_properties(user_that_edits, True, **kwargs)
        return _update_user(user_that_edits)

    if not user_that_edits.admin:
        abort(403, "Non-admins can not edit other users")
    for key in ("login", "language", "user_id", "email"):
        if key in kwargs:
            abort(403, f"You can not edit '{key}' field")

    user = user_repository.get_user_by_id(user_id)
    if not user:
        abort(404, "User not found")
    if user.admin and not user_that_edits.change_admins:
        abort(403, "You can not create, change or delete admins")
    _edit_user_properties(user, False, **kwargs)
    return _update_user(user)
