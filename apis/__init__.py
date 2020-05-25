from flask import Blueprint
from flask_restplus import Api

from .user_api import api as user_api
from .news_api import api as news_api
from .tips_api import api as tips_api
from .forum_api import api as forum_api
from .compilation_api import api as compilation_api

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
    title='Metal In Blood API',
    version='0.1',
    doc='/',
    description='Metal In Blood API <style>.models {display: none !important}</style>',
    authorizations=authorization
)


api.add_namespace(user_api)
api.add_namespace(news_api)
api.add_namespace(tips_api)
api.add_namespace(forum_api)
api.add_namespace(compilation_api)
