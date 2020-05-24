from flask_restplus import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from models.forum_model import (message_full_model, create_message_request_model,
                                thread_full_model, create_thread_request_model, fields)
from services import forum_service, check_page

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


@api.route('/threads')
class Threads(Resource):
    @api.doc('forum_threads', params={'page': 'page number'})
    @api.marshal_with(threads_list, code=200)
    def get(self):
        """Get forum threads"""
        page = request.args.get("page")
        check_page(page)
        return forum_service.get_threads(int(page)), 200

    @api.doc('add_forum_thread', security='apikey')
    @api.expect(create_thread, validate=True)
    @jwt_required
    def post(self):
        """Create forum thread"""
        return forum_service.add_thread(get_jwt_identity(), **api.payload), 201

    @api.doc('delete_forum_thread', params={'id': 'thread ID'}, security='apikey')
    @jwt_required
    def delete(self):
        """Delete forum thread"""
        return forum_service.delete_thread(get_jwt_identity(), request.args.get("id")), 201


@api.route('/threads/search')
class SearchThreads(Resource):
    @api.doc('search_forum_threads', params={'page': 'page number', 'text': 'text to search'})
    @api.marshal_with(threads_list, code=200)
    def get(self):
        """Search forum threads"""
        page = request.args.get("page")
        check_page(page)
        return forum_service.search_threads(int(page), request.args.get("text")), 200


@api.route('/messages')
class ForumMessages(Resource):
    @api.doc('forum_messages', params={'page': 'page number', 'id': 'thread ID'})
    @api.marshal_with(messages_list, code=200)
    def get(self):
        """Get forum thread messages"""
        page = request.args.get("page")
        check_page(page)
        return forum_service.get_messages(int(page), request.args.get("id")), 200

    @api.doc('add_forum_message', security='apikey')
    @api.expect(create_message, validate=True)
    @jwt_required
    def post(self):
        """Create message in forum thread"""
        return forum_service.add_message(get_jwt_identity(), **api.payload), 201

    @api.doc('delete_forum_message', params={'id': 'message ID'}, security='apikey')
    @jwt_required
    def delete(self):
        """Delete message from forum thread"""
        return forum_service.delete_message(get_jwt_identity(), request.args.get("id")), 201


@api.route('/messages/search')
class SearchForumMessages(Resource):
    @api.doc('search_forum_messages', params={'page': 'page number', 'text': 'text to search', 'thread_id': 'thread ID'})
    @api.marshal_with(threads_list, code=200)
    def get(self):
        """Search messages in forum thread"""
        page = request.args.get("page")
        check_page(page)
        return forum_service.search_messages(int(page), request.args.get("thread_id"), request.args.get("text")), 200
