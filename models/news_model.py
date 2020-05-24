from flask_restplus import fields
from .user_model import full_user_model

post_request_model = {
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
    "picture":
        fields.String(
            required=False,
            description='Link to the picture',
            example='https://i.imgur.com/69khNTK.jpg',
            pattern=r'http\S+//\S+\.\S+',
            min_length=4,
            max_length=512
        )
}

post_full_model = {
    "title": post_request_model["title"],
    "body": post_request_model["body"],
    "author":
        full_user_model["user_id"],
    "date":
        fields.Date(
            required=True,
            description='Date in iso8601 format (UTC)',
            example='2005-08-09T18:31:42.201',
            min_length=16,
            max_length=32
        ),
    "picture": post_request_model["picture"],
    "post_id":
        fields.String(
            required=True,
            description='News post unique id in database',
            example='d1d3ee42-731c-04d9-0eee-16d3e7a62948',
            min_length=36,
            max_length=36,
        )
}
