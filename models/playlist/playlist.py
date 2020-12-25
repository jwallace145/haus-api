from database import db
from flask_login.mixins import UserMixin
from sqlalchemy_serializer.serializer import SerializerMixin
from models.playlists_tracks.playlists_tracks import PlaylistsTracks


class Playlist(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'playlists'

    serialize_only = (
        'id',
        'name',
        'spotify_id',
        'cover_url'
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    spotify_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    cover_url = db.Column(db.String, nullable=False)

    user = db.relationship('User')
    tracks = db.relationship(
        'Track', secondary=PlaylistsTracks, backref='playlists', cascade='all,delete')

    def __init__(self, user, name, spotify_id, cover_url):
        self.user = user
        self.name = name
        self.spotify_id = spotify_id
        self.cover_url = cover_url
