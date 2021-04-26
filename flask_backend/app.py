from flask import Flask, jsonify, request, Response, render_template, redirect
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
import flask_login

import json
import pymongo
from urllib.parse import quote
import requests
import os
from dotenv import load_dotenv

from user import User

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/endpoint": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["MONGO_URI"] = "mongodb://localhost:27017/BadDJDatabase"
mongo = PyMongo(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

domain = 'localhost:4000'
AUTH_URL = 'https://accounts.spotify.com/api/token'
REFRESH_URL = 'https://accounts.spotify.com/api/token'
USER_AUTH_URL = 'https://accounts.spotify.com/authorize?client_id=2c8231fad0534937afacccb8a7942d5f&response_type=code&redirect_uri=https://' + domain + '/spotifyAuthCallback&scope=user-read-private user-read-email&state=34fFs29kd09'
USER_ACCESS_URL = 'https://accounts.spotify.com/api/token'


# ========================= OAUTH SETUP ====================================== #

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


# ======================================== TOKENS ===================================== #

def getAccessToken():
    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()
    print(auth_response_data)
    # save the access token
    access_token = auth_response_data['access_token']
    refresh_token = None
    if 'refresh_token' in auth_response_data.keys():
        refresh_token = auth_response_data['refresh_token']
    return {'access_token': access_token, 'refresh_token': refresh_token}

@app.route('/spotifyAuthCallback', methods=['GET'])
def handleSpotifyAuthCallback():
    # TODO: Implement
    auth_code = request.params['code']
    access_response = requests.post(USER_ACCESS_URL, {
        
    })
    return

def getUserAccessToken():
    # TODO: The user needs to be redirected to the spotify URL to authorize the application...
    # TODO: Get access / refresh tokens from the auth token
    return {'access_token': None, 'refresh_token': None}

def refreshUserToken(tokens):
    return refreshToken(tokens, getUserAccessToken)

def refreshToken(tokens, getNewTokens=getAccessToken):
    # First, check to see if we have a refresh token, if not we'll just get a new one the normal way
    if tokens['refresh_token'] == None:
        return getNewTokens()
    # Request a refresh of the token
    refresh_response = requests.post(REFRESH_URL, {
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    # Parse the data
    refresh_response_data = refresh_response.json()
    access_token = refresh_response_data['access_token']
    refresh_token = None
    if 'refresh_token' in refresh_response_data.keys():
        refresh_token = refresh_response_data['refresh_token']
    # And return it
    return {'access_token':access_token,'refresh_token':refresh_token}

tokens = getAccessToken()
access_token = tokens['access_token']
refresh_token = tokens['refresh_token']
tokens = refreshToken(tokens)


# ================================ FLASK SESSIONS ===================================== #

@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.user.find_one({"user_id":user_id})
    if not users:
        return 
    user = User()
    user.user_id = user_id
    return user

def isUnique(id):
    user = mongo.db.users.find_one({"id":id})
    if user:
        return False
    return True

# ============================ OAUTH ================================= #
@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    # playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    # playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    # playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
    display_arr = [profile_data] # + playlist_data["items"]


    # dont add every time
    if isUnique(profile_data["id"]):
        user_db_id = mongo.db.users.insert(profile_data)

    return render_template("index.html", sorted_array=display_arr)


# =============================================================== #


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
