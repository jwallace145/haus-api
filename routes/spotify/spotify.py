from flask import Blueprint, redirect, request, session
from flask_login import current_user, login_required
from models.playlist.playlist import Playlist
from models.track.track import Track
from models.track_rating.track_rating import UsersTracks
from services.database import db
from spotify_requests import spotify

spotify_blueprint = Blueprint('spotify_blueprint', __name__)


@spotify_blueprint.route('/auth', methods=['GET'])
@login_required
def auth():
    return redirect(spotify.AUTH_URL)


@spotify_blueprint.route('/callback', methods=['GET'])
@login_required
def callback():

    auth_token = request.args['code']
    auth_header = spotify.authorize(auth_token)
    session['auth_header'] = auth_header

    return redirect('http://localhost:3000/profile')


@spotify_blueprint.route('/playlists', methods=['GET'])
@login_required
def playlists():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        playlists = spotify.get_users_playlists(auth_header)

        resp = []
        for playlist in playlists['items']:
            new_playlist = Playlist(
                name=playlist['name'],
                spotify_id=playlist['id'],
                cover_url=playlist['images'][0]['url']
            )

            resp.append(new_playlist.to_dict())

            if not db.session.query(Playlist).filter_by(spotify_id=playlist['id']).first():
                db.session.add(new_playlist)
        db.session.commit()

        return {'playlists': resp}


@spotify_blueprint.route('/playlists/<playlist_id>', methods=['GET'])
@login_required
def get_playlist_tracks(playlist_id):
    if 'auth_header' in session:
        auth_header = session['auth_header']

        user = current_user

        tracks = spotify.get_playlist_tracks(auth_header, playlist_id)

        for track in tracks['items']:
            new_track = Track(
                title=track['track']['name'],
                cover_url=track['track']['album']['images'][0]['url']
            )

            if not db.session.query(Track).filter_by(title=track['track']['name']).first():
                user.tracks.append(new_track)
        db.session.commit()

        tracks = db.session.query(Track).filter(
            Track.id == UsersTracks.c.track_id, UsersTracks.c.user_id == user.id)

        return {'tracks': [track.to_dict() for track in tracks]}
    else:
        return {'yup': True}


@spotify_blueprint.route('/tracks', methods=['GET'])
@login_required
def tracks():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        playlists = spotify.get_users_playlists(auth_header)

        playlist_ids = [playlist['id'] for playlist in playlists['items']]

        for playlist_id in playlist_ids:
            tracks = spotify.get_playlist_tracks(auth_header, playlist_id)

            for track in tracks['items']:
                new_track = Track(
                    title=track['track']['name'],
                    cover_url=track['track']['album']['images'][0]['url']
                )

                user = current_user
                user.tracks.append(new_track)
            db.session.commit()

    return {'successful': True}


@spotify_blueprint.route('/ingest', methods=['GET'])
@login_required
def ingest_spotify_data():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        user = current_user

        playlists = spotify.get_users_playlists(auth_header)

        # create playlist and store in db
        new_playlists = []
        for playlist in playlists['items']:
            new_playlist = Playlist(
                name=playlist['name'],
                spotify_id=playlist['id'],
                cover_url=playlist['images'][0]['url']
            )

            if not db.session.query(Playlist).filter_by(spotify_id=new_playlist.spotify_id).first():
                new_playlists.append(new_playlist)
                user.playlists.append(new_playlist)
                db.session.add(new_playlist)
        db.session.commit()

        # get tracks by playlist id and store them in db (associate with playlist)
        new_tracks = []
        for playlist in new_playlists:
            tracks = spotify.get_playlist_tracks(
                auth_header, playlist.spotify_id)

            # get playlist from haus db
            haus_playlist = db.session.query(Playlist).filter_by(
                spotify_id=playlist.spotify_id).first()

            for track in tracks['items']:
                new_track = Track(
                    title=track['track']['name'],
                    cover_url=track['track']['album']['images'][0]['url']
                )

                if not db.session.query(Track).filter_by(title=track['track']['name']).first():
                    new_tracks.append(new_track)
                    a = UsersTracks(rating=5)
                    a.track = new_track
                    user.tracks.append(a)
                    haus_playlist.tracks.append(new_track)
        db.session.commit()

        return {
            'successful': True,
            'playlists': [playlist.to_dict() for playlist in new_playlists],
            'tracks': [track.to_dict() for track in new_tracks]
        }
    else:
        return {'succesful': False}
