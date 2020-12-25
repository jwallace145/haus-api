from database import db
from flask import Blueprint
from flask.globals import request
from flask_login import current_user
from flask_login.utils import login_required
from models.track.track import Track
from models.users_tracks.users_tracks import UsersTracks
from routes.spotify.spotify import tracks

tracks_blueprint = Blueprint('tracks_blueprint', __name__)


@tracks_blueprint.route('/all', methods=['GET'])
def get_all_songs():
    tracks = db.session.query(Track).all()

    return {'tracks': [track.to_dict() for track in tracks]}


@tracks_blueprint.route('/<track_id>/rate', methods=['POST'])
@login_required
def rate_song(track_id):
    rating = request.form['rating']

    user = current_user

    user_track = db.session.query(UsersTracks).filter_by(
        track_id=track_id, user_id=user.id).first()
    user_track.rating = rating
    db.session.commit()

    return {'track': 'successful!'}
