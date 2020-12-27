from services.database import db
from sqlalchemy_serializer import SerializerMixin


class UsersTracks(db.Model, SerializerMixin):
    __tablename__ = 'users_tracks'

    serialize_only = (
        'id',
        'user_id',
        'track_id',
        'rating'
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'))
    rating = db.Column(db.Integer, nullable=False, default=5)

    user = db.relationship('User', back_populates='tracks')
    track = db.relationship('Track', back_populates='users')
