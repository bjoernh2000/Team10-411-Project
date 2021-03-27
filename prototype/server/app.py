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

AUTH_URL = 'https://accounts.spotify.com/api/token'

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
    return access_token

# access_token = getAccessToken()

@app.route("/", methods=["GET"])
def index(): 
    return "HELLO"

@app.route("/postAPI", methods=["POST"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def postAPI():
    apiCall = request.form.get("APICall")
    print(apiCall)
    URL = f"https://api.spotify.com/v1/users/{0}/playlists".format(apiCall)
    PARAMS = {"limit":20, "offset":5}
    
    return "test"

if __name__ == "__main__":
    app.run(port=4000, debug=True)