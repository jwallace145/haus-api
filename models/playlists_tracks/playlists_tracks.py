from database import db

PlaylistsTracks = db.Table(
    'playlists_tracks',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey(
        'playlists.id', ondelete='cascade')),
    db.Column('track_id', db.Integer, db.ForeignKey(
        'tracks.id', ondelete='cascade'))
)
