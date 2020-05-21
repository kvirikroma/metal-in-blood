import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton
from flask_injector import FlaskInjector, Injector
from flask_jwt_extended import JWTManager
from flask_restplus import Api

from apis import api
from frontend_bindings.pages import bind_frontend_pages
from frontend_bindings.errors import bind_error_pages

app = Flask(__name__)
app.register_blueprint(api.blueprint, url_prefix='/api/v1')


class AppModule(Module):
    def __init__(self, flask_app):
        self.app = flask_app
        self.db = SQLAlchemy(flask_app)

    """Configure the application."""

    def configure(self, binder):
        binder.bind(SQLAlchemy, to=self.db, scope=singleton)
        binder.bind(Api, to=api, scope=singleton)
        binder.bind(JWTManager, to=self.configure_jwt(), scope=singleton)
        binder.bind(Flask, to=self.app, scope=singleton)

    def configure_jwt(self):
        jwt = JWTManager(self.app)
        jwt._set_error_handler_callbacks(api)
        return jwt


app.config.update({
    "SWAGGER_UI_DOC_EXPANSION": "list",
    "RESTPLUS_VALIDATE": True,
    "SQLALCHEMY_ECHO": False,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "RESTPLUS_MASK_SWAGGER": False,
    "SECURITY_PASSWORD_HASH": "pbkdf2_sha512"
})

if not (os.environ.get('JWT_KEY') and os.environ.get("PGPASSWORD")):
    raise RuntimeError("Cannot find some env variables related to security")

app.config['SECRET_KEY'] = os.environ.get('JWT_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'postgresql+psycopg2://api:' + os.environ.get("PGPASSWORD") + '@/metalinblood'


bind_frontend_pages(app)
bind_error_pages(app)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
