from flask_restx.namespace import Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from services import forum_service, check_page
from .utils import OptionsResource
from models import pages_count_model, required_query_params
from models.forum_model import (message_full_model, create_message_request_model,
                                thread_full_model, create_thread_request_model, fields)


api = Namespace('forum', description='Forum operations')

message = api.model(
    'message_full_model',
    message_full_model,
)

create_message = api.model(
    'create_message_request_model',
    create_message_request_model,
)

thread = api.model(
    'thread_full_model',
    thread_full_model,
)

create_thread = api.model(
    'create_thread_request_model',
    create_thread_request_model,
)

messages_list = api.model(
    'list_of_thread_messages',
    {
        "messages":
            fields.List(
                fields.Nested(message)
            )
    }
)

threads_list = api.model(
    'list_of_forum_threads',
    {
        "threads":
            fields.List(
                fields.Nested(thread)
            )
    }
)

counted_messages_list = api.model(
    'counted_list_of_thread_messages',
    {
        "messages":
            fields.List(
                fields.Nested(message)
            ),
        "pages_count": pages_count_model
    }
)

counted_threads_list = api.model(
    'counted_list_of_forum_threads',
    {
        "threads":
            fields.List(
                fields.Nested(thread)
            ),
        "pages_count": pages_count_model
    }
)


@api.route('/threads')
class Threads(OptionsResource):
    @api.doc('forum_threads', params=required_query_params({'page': 'page number'}))
    @api.marshal_with(counted_threads_list, code=200)
    def get(self):
        """Get newest forum threads"""
        page = check_page(request)
        return forum_service.get_threads(page), 200

    @api.doc('add_forum_thread', security='apikey')
    @api.expect(create_thread, validate=True)
    @api.response(409, "User already has a thread with this title")
    @api.marshal_with(thread, code=201)
    @jwt_required
    def post(self):
        """Create forum thread"""
        return forum_service.add_thread(get_jwt_identity(), **api.payload), 201

    @api.doc('delete_forum_thread', params=required_query_params({'id': 'thread ID'}), security='apikey')
    @api.response(403, "Non-admin tried to remove thread of other user")
    @api.response(201, "Success")
    @jwt_required
    def delete(self):
        """Delete forum thread"""
        return forum_service.delete_thread(get_jwt_identity(), request.args.get("id")), 201


@api.route('/threads/search')
class SearchThreads(OptionsResource):
    @api.doc('search_forum_threads', params=required_query_params({'page': 'page number', 'text': 'text to search'}))
    @api.marshal_with(threads_list, code=200)
    def get(self):
        """Search forum threads"""
        page = check_page(request)
        return forum_service.search_threads(page, request.args.get("text")), 200


@api.route('/messages')
class ForumMessages(OptionsResource):
    @api.doc('forum_messages', params=required_query_params({'page': 'page number', 'id': 'thread ID'}))
    @api.marshal_with(counted_messages_list, code=200)
    @api.response(404, "Thread not found")
    def get(self):
        """Get forum thread messages"""
        page = check_page(request)
        return forum_service.get_messages(page, request.args.get("id")), 200

    @api.doc('add_forum_message', security='apikey')
    @api.expect(create_message, validate=True)
    @api.response(404, "Thread does not exist")
    @api.response(201, "Success")
    @jwt_required
    def post(self):
        """Create message in forum thread"""
        return forum_service.add_message(get_jwt_identity(), **api.payload), 201

    @api.doc('delete_forum_message', params=required_query_params({'id': 'message ID'}), security='apikey')
    @api.response(404, "Message does not exist")
    @api.response(403, "Non-admin tried to remove message of other user")
    @api.response(201, "Success")
    @jwt_required
    def delete(self):
        """Delete message from forum thread"""
        return forum_service.delete_message(get_jwt_identity(), request.args.get("id")), 201


@api.route('/messages/search')
class SearchForumMessages(OptionsResource):
    @api.doc(
        'search_forum_messages',
        params=required_query_params({'page': 'page number', 'text': 'text to search', 'thread_id': 'thread ID'})
    )
    @api.marshal_with(messages_list, code=200)
    def get(self):
        """Search messages in forum thread"""
        page = check_page(request)
        return forum_service.search_messages(page, request.args.get("thread_id"), request.args.get("text")), 200
