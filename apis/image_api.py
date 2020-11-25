from flask_restx.namespace import Namespace
from flask_restx.reqparse import RequestParser
from flask_restx import fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage

from services import image_service, check_page
from .utils import OptionsResource
from models import pages_count_model, required_query_params
from models.image_model import image_data_model


api = Namespace('image', description='Images uploading and managing')

parser: RequestParser = api.parser()
parser.add_argument('image', location='files',
                    type=FileStorage, required=True)


image_data = api.model(
    'image_data_model',
    image_data_model
)


images_list = api.model(
    'list_of_images',
    {
        "images":
            fields.List(
                fields.Nested(image_data)
            )
    }
)

counted_images_list = api.model(
    'counted_list_of_images',
    {
        "images":
            fields.List(
                fields.Nested(image_data)
            ),
        "pages_count": pages_count_model
    }
)


@api.route('')
class Image(OptionsResource):
    @api.doc("image_upload", security='apikey')
    @api.marshal_with(image_data, code=201)
    @api.response(400, description="Cannot get file from request")
    @api.response(413, description="Image size is too large")
    @api.expect(parser, validate=True)
    @jwt_required
    def post(self):
        """Upload a picture to the server"""
        return image_service.save_image(get_jwt_identity(), request.files.get('image')), 201

    @api.doc("image_download", params=required_query_params({"id": "Image ID"}))
    @api.response(200, description="Success (response contains a requested file)")
    @api.response(404, description="Image not found")
    def get(self):
        """Download a picture from server"""
        return image_service.get_image(request.args.get('id'))

    @api.doc("image_remove", params=required_query_params({"id": "Image ID"}), security='apikey')
    @api.response(201, description="Success")
    @api.response(403, description="Can not delete images of other users")
    @api.response(404, description="Image not found")
    @jwt_required
    def delete(self):
        """Delete a picture from server"""
        image_service.delete_image(get_jwt_identity(), request.args.get('id'))
        return None, 201


@api.route('/all')
class AllImages(OptionsResource):
    @api.doc("get_all_images", params=required_query_params({"page": "page number"}), security='apikey')
    @api.marshal_with(counted_images_list, code=200)
    @jwt_required
    def get(self):
        """Get all pictures of a user"""
        return image_service.get_all_images(get_jwt_identity(), check_page(request))
