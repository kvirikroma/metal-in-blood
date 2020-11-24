from flask_restx.namespace import Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from services import news_service, check_page
from .utils import OptionsResource
from models import pages_count_model
from models.news_model import post_full_model, post_request_model, fields


api = Namespace('news', description='News related operations')

get_news_post = api.model(
    'post_full_model',
    post_full_model,
)

add_news_post = api.model(
    'post_request_model',
    post_request_model,
)

post_list = api.model(
    'list_of_posts',
    {
        "posts":
            fields.List(
                fields.Nested(get_news_post)
            )
    }
)

counted_post_list = api.model(
    'counted_list_of_posts',
    {
        "posts":
            fields.List(
                fields.Nested(get_news_post)
            ),
        "pages_count": pages_count_model
    }
)


@api.route('')
class Posts(OptionsResource):
    @api.doc('newest_posts', params={'page': 'page number'})
    @api.marshal_with(counted_post_list, code=200)
    def get(self):
        """Get newest posts"""
        page = check_page(request)
        return news_service.get_newest_posts(page), 200

    @api.doc('make_new_post', security='apikey')
    @api.expect(add_news_post, validate=True)
    @api.response(201, "Success")
    @api.response(403, "Cannot add a post (don't have a permission)")
    @jwt_required
    def post(self):
        """Make post in news"""
        return news_service.add_post(get_jwt_identity(), **api.payload), 201

    @api.doc('delete_post', params={'post_id': 'post ID'}, security='apikey')
    @api.response(201, "Success")
    @api.response(201, "Tried to remove post of other user")
    @jwt_required
    def delete(self):
        """Delete post from news"""
        return news_service.delete_post(get_jwt_identity(), request.args.get("post_id")), 201


@api.route('/search')
class SearchPosts(OptionsResource):
    @api.doc('search_posts', params={'page': 'page number', 'text': 'text to search'})
    @api.marshal_with(post_list, code=200)
    def get(self):
        """Search posts"""
        page = check_page(request)
        return news_service.search_posts(page, request.args.get("text")), 200
