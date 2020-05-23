from flask_restplus import Namespace, Resource
from flask_jwt_extended import jwt_optional
from flask import request

from models.tip_model import tip_model, fields
from services import tip_service, check_page

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
class Tips(Resource):
    @api.doc('tips', params={'page': 'page number'})
    @api.marshal_with(tips_list, code=200)
    @jwt_optional
    def get(self):
        """Get tips"""
        page = request.args.get("page")
        check_page(page)
        return tip_service.get_tips(int(page)), 200


@api.route('/search')
class Tips(Resource):
    @api.doc('search_tips', params={'page': 'page number', 'text': 'text to search'})
    @api.marshal_with(tips_list, code=200)
    @jwt_optional
    def get(self):
        """Search tips"""
        page = request.args.get("page")
        check_page(page)
        return tip_service.search_tips(int(page), request.args.get("text")), 200
