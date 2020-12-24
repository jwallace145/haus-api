import base64
import json
import os
import urllib.parse as urllibparse

import requests

'''
    --------------------- HOW THIS FILE IS ORGANIZED --------------------
    0. SPOTIFY BASE URL
    1. USER AUTHORIZATION
    2. ARTISTS
    3. SEARCH
    4. USER RELATED REQUETS (NEEDS OAUTH)
    5. ALBUMS
    6. USERS
    7. TRACKS
'''

# ----------------- 0. SPOTIFY BASE URL ---------------- #

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# ----------------- 1. USER AUTHORIZATION ---------------- #

# spotify endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

# client keys
CLIENT_ID = os.getenv('HAUS_CLIENT_ID')
CLIENT_SECRET = os.getenv('HAUS_CLIENT_SECRET')

# server side parameter
CLIENT_SIDE_URL = "http://localhost"
PORT = 8080
REDIRECT_URI = "{}:{}/spotify/callback".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private user-read-recently-played user-top-read"
STATE = ""

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                     for key, val in list(auth_query_parameters.items())])

AUTH_URL = "{}?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)


def authorize(auth_token):
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }

    base64encoded = base64.b64encode(
        ("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())

    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(
        SPOTIFY_TOKEN_URL,
        data=code_payload,
        headers=headers
    )

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}

    return auth_header


# ------------------ 4. USER RELATED REQUESTS  ---------- #

# spotify endpoints
USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT = "{}/{}".format(
    USER_PROFILE_ENDPOINT, 'top')  # /<type>
USER_RECENTLY_PLAYED_ENDPOINT = "{}/{}/{}".format(USER_PROFILE_ENDPOINT,
                                                  'player', 'recently-played')
BROWSE_FEATURED_PLAYLISTS = "{}/{}/{}".format(SPOTIFY_API_URL, 'browse',
                                              'featured-playlists')


def get_users_profile(auth_header):
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_users_playlists(auth_header):
    url = USER_PLAYLISTS_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_playlist_tracks(auth_header, track_id):
    url = SPOTIFY_API_URL + f'/playlists/{track_id}/tracks'
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_users_top(auth_header, t):
    if t not in ['artists', 'tracks']:
        print('invalid type')
        return None
    url = "{}/{type}".format(USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT, type=t)
    resp = requests.get(url, headers=auth_header)
    print(resp)


def get_users_recently_played(auth_header):
    url = USER_RECENTLY_PLAYED_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_featured_playlists(auth_header):
    url = BROWSE_FEATURED_PLAYLISTS
    resp = requests.get(url, headers=auth_header)
    return resp.json()
