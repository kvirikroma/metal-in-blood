from flask_restx.namespace import Namespace
from flask_restx.reqparse import RequestParser
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage

from services import compilation_service, check_page
from .utils import OptionsResource


api = Namespace('compilations', description='Albums and YouTube compilations')

parser: RequestParser = api.parser()
parser.add_argument('file', location='files',
                    type=FileStorage, required=True)


