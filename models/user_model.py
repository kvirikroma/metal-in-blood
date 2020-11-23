from enum import Enum

from flask_restplus import fields


class Language(Enum):
    en = 0
    ua = 1


sign_up_model = {
    "email":
        fields.String(
            required=True,
            description='User email to log in',
            example='test@mail.com',
            pattern=r'\S+@\S+\.\S+',
            min_length=5,
            max_length=256
        ),
    "login":
        fields.String(
            required=True,
            description='Unique username to find user by it',
            example='MetalHead1337',
            min_length=3,
            max_length=32
        ),
    "password":
        fields.String(
            required=True,
            description='User\'s password to log in',
            example='Qwerty123',
            min_length=8,
            max_length=64
        )
}

sign_in_model = {
    "login": sign_up_model["login"],
    "password": sign_up_model["password"]
}

full_user_model = sign_up_model.copy()
full_user_model.update({
    "user_id":
        fields.String(
            required=True,
            description="User's unique id in database",
            example='d1d3ee42-731c-04d9-0eee-16d3e7a62948',
            min_length=36,
            max_length=36,
        ),
    "admin":
        fields.Boolean(
            required=False,
            description="Is the user an administrator",
            example=False,
        ),
    "change_admins":
        fields.Boolean(
            required=False,
            description="The user's ability to change other admins' privileges",
            example=False,
        ),
    "change_tips":
        fields.Boolean(
            required=False,
            description="The user's ability to add or remove tips",
            example=False,
        ),
    "change_news":
        fields.Boolean(
            required=False,
            description="The user's ability to add or remove news posts",
            example=False,
        ),
    "change_compilations":
        fields.Boolean(
            required=False,
            description="The user's ability to add or remove compilations or albums",
            example=False,
        ),
    "language":
        fields.String(
            required=False,
            description="The user's preferred language",
            example="en",
            enum=[lang.name for lang in Language],
        )
})

token_model = {
    'access_token':
        fields.String(
            required=True,
            description='Token to access resources',
            example='qwerty',
        ),
    'refresh_token':
        fields.String(
            required=True,
            description='Token to refresh pair of tokens',
            example='qwerty',
        ),
    "user_id":
        full_user_model["user_id"]
}

user_characteristics_model = full_user_model.copy()
del user_characteristics_model["password"]
del user_characteristics_model["email"]

user_edit_model = user_characteristics_model.copy()
del user_edit_model["user_id"]
user_edit_model["login"] = fields.String(
    required=False,
    description='Unique username to find user by it',
    example='MetalHead1337',
    min_length=3,
    max_length=32
)
