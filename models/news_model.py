from flask_restplus import fields
from .user_model import full_user_model

news_search_request_model = {
    "text":
        fields.String(
            required=True,
            description='Text to search',
            example='guitar',
            min_length=2,
            max_length=32
        )
}

post_model = {
    "title":
        fields.String(
            required=True,
            description='Title of post',
            example="Erra's new album",
            min_length=2,
            max_length=64
        ),
    "body":
        fields.String(
            required=True,
            description='Post body',
            example='Check out the new album of Erra band!',
            min_length=4,
            max_length=8192
        ),
    "author":
        full_user_model["user_id"],
    "date":
        fields.Date(
            required=True,
            description='Date in iso8601 format',
            example='2005-08-09T18:31:42.201',
            min_length=16,
            max_length=32
        ),
    "picture":
        fields.String(
            required=False,
            description='Link to the picture',
            example='https://i.imgur.com/69khNTK.jpg',
            pattern=r'\h\t\t\p\S+\/\/\S+\.\S+',
            min_length=4,
            max_length=512
        )
}
