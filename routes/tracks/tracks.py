from flask import Blueprint
from database import db
from models.track.track import Track

tracks_blueprint = Blueprint('tracks_blueprint', __name__)


@tracks_blueprint.route('/all', methods=['GET'])
def get_all_songs():
    tracks = db.session.query(Track).all()

    return {'tracks': [track.to_dict() for track in tracks]}
