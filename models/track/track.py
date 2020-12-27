from services.database import db
from sqlalchemy_serializer.serializer import SerializerMixin


class Track(db.Model, SerializerMixin):
    __tablename__ = 'tracks'

    serialize_only = (
        'id',
        'title',
        'cover_url'
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    cover_url = db.Column(db.String, nullable=False)

    users = db.relationship('UsersTracks', back_populates='track')

    def __init__(self, title, cover_url):
        self.title = title
        self.cover_url = cover_url
