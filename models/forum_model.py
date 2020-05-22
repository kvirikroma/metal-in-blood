from flask_restplus import fields
from .news_model import post_model


create_thread_request_model = {
    "title":
        fields.String(
            required=True,
            description='Title of the thread',
            example='How to mosh correctly?',
            min_length=4,
            max_length=64
        ),
    "body":
        fields.String(
            required=True,
            description='Text of the main thread message',
            example='Can anyone help me to figure out some theory?',
            min_length=4,
            max_length=8192
        )
}

thread_full_model = create_thread_request_model.copy()
thread_full_model.update({
    "author": post_model["author"],
    "date": post_model["date"],
    "thread_id":
        fields.String(
            required=True,
            description='Unique id of forum thread',
            example='d1d3ee42-731c-04d9-0eee-16d3e7a62948',
            min_length=4,
            max_length=8192
        )
})


create_message_request_model = {
    "body":
        fields.String(
            required=True,
            description='Text of the main thread message',
            example='Can anyone help me to figure out some theory?',
            min_length=4,
            max_length=8192
        ),
    "related_to": thread_full_model["thread_id"],
}

message_full_model = create_message_request_model.copy()
message_full_model.update({
    "author": post_model["author"],
    "date": post_model["date"]
})
