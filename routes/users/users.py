from flask import Blueprint, request, session
from flask_login import current_user, login_required
from models.playlist.playlist import Playlist
from models.track.track import Track
from models.user.user import User
from models.track_rating.track_rating import UsersTracks
from services.database import db
from flask_login import AnonymousUserMixin

users_blueprint = Blueprint('users_blueprint', __name__)


@users_blueprint.route('/current', methods=['GET'])
def get_user():
    user = current_user

    if user.is_authenticated:
        return {
            'exists': True,
            'user': user.to_dict()
        }
    else:
        return {'exists': False}


@users_blueprint.route('/edit', methods=['GET'])
def edit_user():
    user = db.session.query(User).filter_by(
        username=request.form['username']).first()

    if user:
        return {}
    else:
        return {
            'edit': False,
            'user': 'does not exist'
        }


@users_blueprint.route('/tracks', methods=['GET'])
@login_required
def get_songs():
    user = current_user
    tracks = db.session.query(
        Track.id,
        Track.title,
        Track.cover_url,
        UsersTracks.rating
    ).filter(
        Track.id == UsersTracks.track_id,
        UsersTracks.user_id == user.id
    )

    resp = []
    for track in tracks:
        resp.append({
            'id': track.id,
            'title': track.title,
            'cover_url': track.cover_url,
            'rating': track[3]
        })

    if tracks:
        return {'tracks': resp}
    else:
        return {'tracks': False}


@users_blueprint.route('/playlists', methods=['GET'])
def get_user_playlists():
    user = current_user

    playlists = db.session.query(Playlist).filter_by(user_id=user.id)

    return {'playlists': [playlist.to_dict() for playlist in playlists]}
