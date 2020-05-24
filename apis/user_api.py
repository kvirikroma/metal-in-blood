from flask_restplus import Namespace, Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, create_access_token, create_refresh_token

from models.user_model import sign_up_model, full_user_model, sign_in_model, token_model
from services import user_service

api = Namespace('user', description='User account related operations')

sign_up = api.model(
    'sign_up_model',
    sign_up_model,
)

full_user = api.model(
    'full_user_model',
    full_user_model,
)

sign_in = api.model(
    'sign_in_model',
    sign_in_model,
)

token = api.model(
    'token_model',
    token_model,
)


@api.route('/signup')
class SignUp(Resource):
    @api.doc('sign_up')
    @api.expect(sign_up, validate=True)
    def post(self):
        """Create an account"""
        return user_service.register_user(**api.payload), 201


@api.route('/signin')
class SignIn(Resource):
    @api.doc('sign_in')
    @api.expect(sign_in, validate=True)
    @api.marshal_with(token, code=200)
    def post(self):
        """Log into an account"""
        return user_service.get_token(**api.payload), 200


@api.route('/refresh')
class RefreshToken(Resource):
    @api.doc('refresh_token')
    @api.marshal_with(token, code=200)
    @jwt_refresh_token_required
    def post(self):
        """Refresh user's pair of tokens"""
        identity = get_jwt_identity()
        return {
            'access_token': create_access_token(identity=identity),
            'refresh_token': create_refresh_token(identity=identity),
            'user_id': identity
        }, 200
