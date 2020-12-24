from database import db
from flask import Blueprint, session
from flask_login import login_required, current_user
from models.track.track import Track
from models.user.user import User
from models.users_tracks.users_tracks import UsersTracks

users_blueprint = Blueprint('users_blueprint', __name__)


@users_blueprint.route('/current', methods=['GET'])
@login_required
def get_user():
    user = current_user
    return {'user': user.to_dict()}


@users_blueprint.route('/tracks', methods=['GET'])
@login_required
def get_songs():
    user = current_user
    tracks = db.session.query(
        Track
    ).filter(
        Track.id == UsersTracks.c.track_id,
        UsersTracks.c.user_id == user.id
    )
    return {'tracks': [track.to_dict() for track in tracks]}
