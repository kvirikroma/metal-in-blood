from flask import Blueprint
from flask_restplus import Api

api_bp = Blueprint('api', __name__)

authorization = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    api_bp,
    title='Metal_In_Blood API',
    version='0.1',
    doc='/',
    description='Metal_In_Blood API <style>.models {display: none !important}</style>',
    authorizations=authorization
)


