from flask_restplus import fields
from .news_model import news_search_request_model

tip_model = {
    "title":
        fields.String(
            required=True,
            description='Title of the tip',
            example='Slam rules',
            min_length=4,
            max_length=64
        ),
    "body":
        fields.String(
            required=True,
            description='Text of the tip',
            example='MetalHead1337',
            min_length=4,
            max_length=8192
        ),
    "tip_id":
        fields.String(
            required=True,
            description='Tip id to request picture for it',
            example='d1d3ee42-731c-04d9-0eee-16d3e7a62948',
            min_length=36,
            max_length=36,
        )
}

tip_search_request_model = news_search_request_model.copy()
