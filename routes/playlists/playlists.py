from database import db
from flask import Blueprint
from models.playlist.playlist import Playlist

playlists_blueprint = Blueprint('playlists_blueprint', __name__)


@playlists_blueprint.route('/all', methods=['GET'])
def get_playlists():

    playlists = db.session.query(Playlist).all()

    return {'playlists': [playlist.to_dict() for playlist in playlists]}
