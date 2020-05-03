"""The app module contains the app factory function."""
import os

from flask import Flask, url_for, current_app

from . import extensions
from . import settings
from . import api, user, public
from flask_socketio import SocketIO

app_runner = SocketIO()

@app_runner.on('connect','/live_connect')
def handle_socket_connect():
    print('Connected to socket')

@app_runner.on('disconnect','/live_connect')
def handle_socket_connect():
    print('Disconnected to socket')

@app_runner.on('my event')
def handle_my_event(data):
    print('received data {}'.format(data))


def create_app(config=settings.ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extentions(app)
    register_blueprints(app)

    return app


def register_extentions(app):
    extensions.login_manager.init_app(app)
    extensions.csrf.init_app(app)
    app_runner.init_app(app)

def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
