from flask import Blueprint, current_app
from flask_restx import Api

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


class CustomApi(Api):
    def handle_error(self, e):
        for val in current_app.error_handler_spec.values():
            for handler in val.values():
                registered_error_handlers = list(filter(lambda x: isinstance(e, x), handler.keys()))
                if len(registered_error_handlers) > 0:
                    raise e
        return super().handle_error(e)


api = CustomApi(
    api_bp,
    title='Metal In Blood API',
    version='0.1.1',
    doc='/',
    description='Metal In Blood API',
    authorizations=authorization
)


api.namespaces.clear()
api.add_namespace(user_api)
api.add_namespace(news_api)
api.add_namespace(tips_api)
api.add_namespace(forum_api)
api.add_namespace(compilation_api)

cors_headers = {
    'Access-Control-Allow-Origin': "*",
    "Access-Control-Allow-Headers":
        "Access-Control-Allow-Headers, "
        "Origin, Accept, "
        "X-Requested-With, "
        "Content-Type, "
        "Access-Control-Request-Method, "
        "Access-Control-Request-Headers",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST, PUT"
}
