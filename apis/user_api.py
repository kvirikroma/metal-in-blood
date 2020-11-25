from flask import request
from flask_restx.namespace import Namespace
from flask_jwt_extended import (jwt_refresh_token_required, get_jwt_identity, jwt_optional,
                                create_access_token, create_refresh_token, jwt_required)

from services import user_service
from .utils import OptionsResource
from models import required_query_params
from models.user_model import (sign_up_model, full_user_model, sign_in_model, token_model,
                               user_characteristics_model, user_edit_model)


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

user_characteristics = api.model(
    'user_characteristics_model',
    user_characteristics_model
)

user_edit = api.model(
    'user_edit_model',
    user_edit_model
)


@api.route('/signup')
class SignUp(OptionsResource):
    @api.doc('sign_up')
    @api.response(201, "Success")
    @api.response(409, "Username or email exists")
    @api.expect(sign_up, validate=True)
    def post(self):
        """Create an account"""
        return user_service.register_user(**api.payload), 201


@api.route('/signin')
class SignIn(OptionsResource):
    @api.doc('sign_in')
    @api.expect(sign_in, validate=True)
    @api.response(401, "Invalid credentials given")
    @api.response(404, "User not found")
    @api.marshal_with(token, code=200)
    def post(self):
        """Log into an account"""
        return user_service.get_token(**api.payload), 200


@api.route('/refresh')
class RefreshToken(OptionsResource):
    @api.doc('refresh_token', security='apikey')
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


@api.route('')
class Account(OptionsResource):
    @api.doc('get_account', params=required_query_params({'id': 'user ID'}))
    @api.response(404, "User not found")
    @api.marshal_with(user_characteristics, code=200)
    @jwt_optional
    def get(self):
        """Get user's account info"""
        user_id = get_jwt_identity()
        if not user_id:
            user_id = request.args.get("id")
        return user_service.get_user(user_id)

    edit_user_403_description = "May appear on multiple reasons:\n"\
        "1. You can not change your own privileges\n"\
        "2. Non-admins can not edit other users\n"\
        "3. You can not edit some field\n"\
        "4. You don't have permission to create, change or delete admins\n"

    @api.doc('edit_account', params=required_query_params({'id': 'user ID'}), security='apikey')
    @api.response(404, "User not found")
    @api.response(403, edit_user_403_description)
    @api.response(422, "Incorrect user configuration is given")
    @api.marshal_with(user_characteristics, code=201)
    @api.expect(user_edit, validate=True)
    @jwt_required
    def put(self):
        """Edit user's account info"""
        return user_service.edit_user(get_jwt_identity(), request.args.get("id"), **api.payload), 201

    @api.doc('delete_account', params=required_query_params({'id': 'user ID'}), security='apikey')
    @api.response(404, "User not found")
    @api.response(403, "Cannot delete this account")
    @api.marshal_with(user_characteristics, code=201)
    @jwt_required
    def delete(self):
        """Delete user's account"""
        return user_service.delete_user(get_jwt_identity(), request.args.get("id")), 201
