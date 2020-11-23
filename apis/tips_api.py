from flask_restplus.namespace import Namespace
from flask import request

from flask_jwt_extended import jwt_required, get_jwt_identity

from services import tip_service, check_page
from .utils import OptionsResource
from models.tip_model import tip_model, fields


api = Namespace('tips', description='Tips related operations')

tip = api.model(
    'tip_model',
    tip_model,
)

tips_list = api.model(
    'list_of_tips',
    {
        "tips":
            fields.List(
                fields.Nested(tip)
            )
    }
)


@api.route('')
class Tips(OptionsResource):
    @api.doc('tips', params={'page': 'page number'})
    @api.marshal_with(tips_list, code=200)
    def get(self):
        """Get tips"""
        page = check_page(request)
        return tip_service.get_tips(page), 200

    @api.doc('add_tip', security='apikey')
    @api.marshal_with(tip, code=201)
    @api.response(403, "Don't have a permission to add tips")
    @api.expect(tip, validate=True)
    @jwt_required
    def post(self):
        """Add a tip"""
        return tip_service.add_tip(get_jwt_identity(), **api.payload)

    @api.doc('remove_tip', params={'id': 'tip ID'}, security='apikey')
    @api.response(201, "Success")
    @api.response(403, "Don't have a permission to remove tips")
    @jwt_required
    def delete(self):
        """Remove a tip"""
        return tip_service.delete_tip(get_jwt_identity(), request.args.get("id"))


@api.route('/search')
class SearchTips(OptionsResource):
    @api.doc('search_tips', params={'page': 'page number', 'text': 'text to search'})
    @api.marshal_with(tips_list, code=200)
    def get(self):
        """Search tips"""
        page = check_page(request)
        return tip_service.search_tips(page, request.args.get("text")), 200
