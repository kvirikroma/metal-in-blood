import os
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton
from flask_jwt_extended import JWTManager
from flask_restplus import Api
from flask_injector import FlaskInjector

from apis import api
from frontend_bindings.pages import bind_frontend_pages
from frontend_bindings.errors import bind_error_pages

app = Flask(__name__)
app.register_blueprint(api.blueprint, url_prefix='/api/v1')


with open(os.path.join(app.root_path, 'config.json'), 'r') as config_file:
    app.config.update(json.loads(config_file.read()))

if not (os.environ.get('JWT_KEY') and os.environ.get("PGPASSWORD")):
    raise RuntimeError("Cannot find some env variables related to security")

app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY'] = os.environ.get('JWT_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'postgresql+psycopg2://mib_api:' + os.environ.get("PGPASSWORD") + '@/metalinblood'


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
        jwt._set_error_handler_callbacks(api)  # This is needed to automatically send 401 on token expiration
        return jwt


FlaskInjector(app=app, modules=[AppModule(app)])
bind_frontend_pages(app)
bind_error_pages(app)


if __name__ == "__main__":
    # app.config["JWT_ACCESS_TOKEN_EXPIRES"] *= 32
    app.run(debug=True, host='0.0.0.0', port=5000)
