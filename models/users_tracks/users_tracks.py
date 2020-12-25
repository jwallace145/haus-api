from database import db

UsersTracks = db.Table(
    'users_tracks',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade')),
    db.Column('track_id', db.Integer, db.ForeignKey(
        'tracks.id', ondelete='cascade')),
    db.Column('rating', db.Integer, nullable=False, default=5)
)
