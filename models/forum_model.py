from flask_restplus import fields

from .user_model import full_user_model


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
    "author": full_user_model["login"],
    "date":
        fields.DateTime(
            required=True,
            description='Date and time in iso8601 format (UTC)',
            example='2005-08-09T18:31:42.201',
            min_length=16,
            max_length=32
        ),
    "thread_id":
        fields.String(
            required=True,
            description='Unique id of forum thread',
            example='d1d3ee42-731c-04d9-0eee-16d3e7a62948',
            min_length=36,
            max_length=36
        ),
    "users_count":
        fields.Integer(
            required=True,
            description='Count of participants in the thread',
            example=2,
            min=0
        ),
    "messages_count":
        fields.Integer(
            required=True,
            description='Count of messages in the thread',
            example=3,
            min=0
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
    "author": full_user_model["login"],
    "date": thread_full_model["date"],
    "message_id":
        fields.String(
            required=True,
            description='Unique id of forum message',
            example='d1d3ee42-731c-04d9-0eee-16d3e7a62948',
            min_length=36,
            max_length=36
        )
})
