from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/endpoint": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

domain = 'localhost:4000'
AUTH_URL = 'https://accounts.spotify.com/api/token'
REFRESH_URL = 'https://accounts.spotify.com/api/token'
USER_AUTH_URL = 'https://accounts.spotify.com/authorize?client_id=2c8231fad0534937afacccb8a7942d5f&response_type=code&redirect_uri=https://' + domain + '/spotifyAuthCallback&scope=user-read-private user-read-email&state=34fFs29kd09'
USER_ACCESS_URL = 'https://accounts.spotify.com/api/token'

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

@app.route("/", methods=["GET"])
def index(): 
    return "HELLO"

@app.route("/postAPI", methods=["POST"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def postAPI():
    apiCall = request.form.get("APICall")
    print(apiCall)
    URL = "https://api.spotify.com/v1/users/{0}/playlists".format(apiCall)
    print(URL)
    PARAMS = {"limit":20}
    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    
    getReq = requests.get(url=URL, params=PARAMS, headers=headers)
    print(getReq.json())
    return getReq.json()

if __name__ == "__main__":
    app.run(port=4000, debug=True)
