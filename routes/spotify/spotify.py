from models.users_tracks.users_tracks import UsersTracks
import requests
from database import db
from flask import Blueprint, redirect, request, session
from flask_login import current_user, login_required
from models.track.track import Track
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
            resp.append({
                'playlist_id': playlist['id'],
                'playlist_name': playlist['name']
            })

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

            user.tracks.append(new_track)
        db.session.commit()

        tracks = db.session.query(Track).filter(
            Track.id == UsersTracks.c.track_id, UsersTracks.c.user_id == user.id)

        return {'tracks': [track.to_dict() for track in tracks]}
    else:
        return {'yup': True}


@ spotify_blueprint.route('/tracks', methods=['GET'])
@ login_required
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
