import os

from flask import Flask
from flask_cors import CORS

from auth import login_manager
from database import db
from routes.auth.auth import auth_blueprint
from routes.spotify.spotify import spotify_blueprint
from routes.tracks.tracks import tracks_blueprint
from routes.users.users import users_blueprint


def create_app():

    # create flask app
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_SETTINGS'))

    # enable CORS, support credentials
    CORS(app, supports_credentials=True)

    # initialize db
    db.init_app(app)

    # initialize login manager
    login_manager.init_app(app)

    # register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(spotify_blueprint, url_prefix='/spotify')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(tracks_blueprint, url_prefix='/tracks')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
