from flask_restx.namespace import Namespace
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from services import compilation_service, check_page
from .utils import OptionsResource
from models.compilation_model import album_model, yt_compilation_model, fields


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
class Albums(OptionsResource):
    @api.doc('albums', params={'page': 'page number'})
    @api.marshal_with(albums_list, code=200)
    def get(self):
        """Get albums"""
        page = check_page(request)
        return compilation_service.get_albums(page), 200

    @api.doc('add_album', security='apikey')
    @api.marshal_with(album, code=201)
    @api.response(403, "Don't have a permission to add albums or compilations")
    @api.expect(album, validate=True)
    @jwt_required
    def post(self):
        """Add an album"""
        return compilation_service.add_album(get_jwt_identity(), **api.payload)

    @api.doc('remove_album', params={'id': 'album ID'}, security='apikey')
    @api.response(201, "Success")
    @api.response(403, "Don't have a permission to remove albums or compilations")
    @jwt_required
    def delete(self):
        """Remove an album"""
        return compilation_service.delete_album(get_jwt_identity(), request.args.get("id"))


@api.route('/albums/search')
class SearchAlbums(OptionsResource):
    @api.doc('search_albums', params={'page': 'page number', 'text': 'text to search'})
    @api.marshal_with(albums_list, code=200)
    def get(self):
        """Search albums"""
        page = check_page(request)
        return compilation_service.search_albums(page, request.args.get("text")), 200


@api.route('/yt')
class Compilations(OptionsResource):
    @api.doc('yt_compilations', params={'page': 'page number'})
    @api.marshal_with(yt_compilations_list, code=200)
    def get(self):
        """Get YouTube compilations"""
        page = check_page(request)
        return compilation_service.get_compilations(page), 200

    @api.doc('add_compilation', security='apikey')
    @api.marshal_with(yt_compilation, code=201)
    @api.response(403, "Don't have a permission to add albums or compilations")
    @api.expect(yt_compilation, validate=True)
    @jwt_required
    def post(self):
        """Add a compilation"""
        return compilation_service.add_compilation(get_jwt_identity(), **api.payload)

    @api.doc('remove_compilation', params={'id': 'compilation ID'}, security='apikey')
    @api.response(201, "Success")
    @api.response(403, "Don't have a permission to remove albums or compilations")
    @jwt_required
    def delete(self):
        """Remove a compilation"""
        return compilation_service.delete_compilation(get_jwt_identity(), request.args.get("id"))


@api.route('/yt/search')
class SearchCompilations(OptionsResource):
    @api.doc('search_yt_compilations', params={'page': 'page number', 'text': 'text to search'})
    @api.marshal_with(yt_compilations_list, code=200)
    def get(self):
        """Search YouTube compilations"""
        page = check_page(request)
        return compilation_service.search_compilations(page, request.args.get("text")), 200
