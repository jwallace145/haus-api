import datetime as dt

from sqlalchemy.orm import backref

from database import db
from flask_login import UserMixin
from models.users_tracks.users_tracks import UsersTracks
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    serialize_only = (
        'id',
        'email',
        'username',
        'authenticated',
        'created_on',
        'last_login',
        'avatar_url'
    )

    serialize_rules = (
        '-password',
    )

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.Binary, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    avatar_url = db.Column(db.String, nullable=False,
                           default='default avatar url')

    tracks = db.relationship(
        'Track', secondary=UsersTracks, backref='users', cascade='all,delete')
    playlists = db.relationship("Playlist", backref='users')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        self.created_on = dt.datetime.utcnow()
        self.last_login = dt.datetime.utcnow()
