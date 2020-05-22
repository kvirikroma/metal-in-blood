from flask_restplus import Namespace, Resource
from flask_jwt_extended import jwt_optional
from flask import request

from models.compilation_model import album_model, yt_compilation_model, fields
from services import compilation_service, check_page

api = Namespace('compilations', description='Albums and YouTube compilations')

album = api.model(
    'album_model',
    album_model,
)

yt_compilation = api.model(
    'yt_compilation_model',
    yt_compilation_model,
)

albums_list = api.model(
    'list_of_albums',
    {
        "albums":
            fields.List(
                fields.Nested(album)
            )
    }
)

yt_compilations_list = api.model(
    'list_of_yt_compilations',
    {
        "compilations":
            fields.List(
                fields.Nested(yt_compilation)
            )
    }
)


@api.route('/albums')
class Albums(Resource):
    @api.doc('albums', params={'page': 'page number'})
    @api.marshal_with(albums_list, code=200)
    @jwt_optional
    def get(self):
        """Get albums"""
        page = request.args.get("page")
        check_page(page)
        return compilation_service.get_albums(int(page)), 200


@api.route('/albums/search')
class SearchAlbums(Resource):
    @api.doc('search_albums', params={'page': 'page number', 'text': 'text to search'})
    @api.marshal_with(albums_list, code=200)
    @jwt_optional
    def get(self):
        """Search albums"""
        page = request.args.get("page")
        check_page(page)
        return compilation_service.search_albums(int(page), request.args.get("text")), 200


@api.route('/yt')
class Compilations(Resource):
    @api.doc('yt_compilations', params={'page': 'page number'})
    @api.marshal_with(yt_compilations_list, code=200)
    @jwt_optional
    def get(self):
        """Get YouTube compilations"""
        page = request.args.get("page")
        check_page(page)
        return compilation_service.get_compilations(int(page)), 200


@api.route('/yt/search')
class SearchCompilations(Resource):
    @api.doc('search_yt_compilations', params={'page': 'page number', 'text': 'text to search'})
    @api.marshal_with(yt_compilations_list, code=200)
    @jwt_optional
    def get(self):
        """Search YouTube compilations"""
        page = request.args.get("page")
        check_page(page)
        return compilation_service.search_compilations(int(page), request.args.get("text")), 200
