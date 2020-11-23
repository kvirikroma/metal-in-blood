from flask_restplus import Resource
from flask_restplus.namespace import Namespace


api = Namespace("")


class OptionsResource(Resource):
    @api.hide
    def options(self):
        return None, 200
