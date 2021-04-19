from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
import requests
import os
import itertools
import math
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/endpoint": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["MONGO_URI"] = "mongodb://localhost:27017/BadDJDatabase"
mongo = PyMongo(app)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
LAST_FM_API_KEY = os.environ.get("LAST_FM_API_KEY")

domain = 'localhost:4000'
AUTH_URL = 'https://accounts.spotify.com/api/token'
REFRESH_URL = 'https://accounts.spotify.com/api/token'
USER_AUTH_URL = 'https://accounts.spotify.com/authorize?client_id=2c8231fad0534937afacccb8a7942d5f&response_type=code&redirect_uri=https://' + domain + '/spotifyAuthCallback&scope=user-read-private user-read-email&state=34fFs29kd09'
USER_ACCESS_URL = 'https://accounts.spotify.com/api/token'
SIMILAR_TRACKS_URL = 'http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={1}&track={0}&api_key={2}&autocorrect=1&limit=3&format=json'
TOP_TAGS_URL = 'https://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={1}&track={0}&api_key={2}&format=json'
SIMILAR_TAGS_URL = 'http://ws.audioscrobbler.com/2.0/?method=tag.getsimilar&tag={0}&api_key={1}&format=json'

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


# == Last.FM API methods == #
	
def getSimilarTracks(song, artist):
	api_response = requests.get(SIMILAR_TRACKS_URL.format(song, artist, LAST_FM_API_KEY)).json()
	return [song['name'] for song in api_response['similartracks']['track']]

def getTrackTopTags(song, artist):
	api_response = requests.get(TOP_TAGS_URL.format(song, artist, LAST_FM_API_KEY)).json()
	return api_response['toptags']['tag']


# == Methods to get the user's top X == #

def getUserRankedSongs(user):
	# This might want to be implemented in a way that takes the user's listening habits into account
	return getUserSongs(user)

def getUserRankedSimilarSongs(user, songs = None):
	if songs == None:
		songs = getUserSongs(user)
	unflattened_similar_songs = [getSimilarTracks(song['title'], song['artist']) for song in songs]
	return list(dict.fromkeys(list(itertools.chain(*unflattened_similar_songs))))

def getUserRankedTags(user, songs = None):
	if songs == None:
		songs = getUserSongs(user)
	uncombined_tags = [getTrackTopTags(song['title'], song['artist']) for song in songs]
	tag_scores = {}
	for song_tags in uncombined_tags:
		temp_counts = {}
		max_count = 1
		for i in range(len(song_tags)):
			tag_name = song_tags[i]['name']
			if tag_name not in temp_counts:
				temp_counts[tag_name] = 0
			temp_counts[tag_name] += song_tags[i]['count']
			max_count = max(max_count, song_tags[i]['count'])
		for tag_name in temp_counts.keys():
			if tag_name not in tag_scores:
				tag_scores[tag_name] = 0
			tag_scores[tag_name] += temp_counts[tag_name] / max_count
	tags = orderedListFromDictOfScores(tag_scores)
	return tags
	
# == Friend recommendations etc == #

def getSimilarUsers(user, include_scores = False):
	# Can't get this info directly from Last.FM,
	# but can get track, similar tracks, and tag
	# info for a user's songs, then use that to 
	# determine how similar they are.
	# Step 1) Get data from Last.FM for the current user
	songs = getUserRankedSongs(user)
	similar_songs = getUserRankedSimilarSongs(user, songs=songs)
	tags = getUserRankedTags(user, songs=songs)
	# Step 2) Calculate similarity scores
	# TODO: Numbers might need to be tweaked
	similar_users = {}
	all_users = getAllUsers()
	for other_user in all_users:
		if other_user == user:
			continue
		# This data should *really* be stored in the database so this isn't hitting the Last.FM API so many times per recommendation
		other_user_songs = getUserRankedSongs(other_user)
		other_user_tags = getUserRankedTags(other_user)
		similarity_score = 1.0 * rankedListSimilarity(songs, other_user_songs) + 0.8 * rankedListSimilarity(similar_songs, other_user_songs) + 0.5 * rankedListSimilarity(tags, other_user_tags)
		similar_users[other_user] = similarity_score
	if not include_scores:
		return orderedListFromDictOfScores(similar_users)
	else:
		return sortDict(similar_users)

# == Utility == #

def orderedListFromDictOfScores(a):
	return [x[0] for x in sorted(a.items(),key=lambda item:item[1],reverse=True)]

def sortDict(a):
	return sorted(a.items(),key=lambda item:item[1],reverse=True)

def rankedListSimilarity(a, b):
	# TODO: Might want to swap this out for a different algorithm... using a custom one at the moment
	similarity = 0.0
	for i in range(len(a)):
		val = a[i]
		if val not in b:
			continue
		j = b.index(val)
		similarity += math.sqrt((len(a)-i)/float(len(a))*(len(b)-j)/float(len(b)))
	return similarity / float(len(a))

# == User management == #

def getAllUsers():
	return ['testUserA', 'testUserB', 'testUserC', 'testUserD']

def getUserSongs(user):
	# TODO: Implement!
	if user == "testUserA":
		return [{'title':'19-2000','artist':'gorillaz'},{'title':'feel good inc.','artist':'gorillaz'}]
	elif user == "testUserB":
		return [{'title':'on melancholy hill','artist':'gorillaz'},{'title':'Yellow Submarine','artist':'the beatles'}]
	elif user == "testUserC":
		return [{'title':'every planet we reach is dead','artist':'gorillaz'}]
	elif user == "testUserD":
		return [{'title':'hey jude','artist':'the beatles'}]
	else:
		return None

# == App code == #

tokens = getAccessToken()
access_token = tokens['access_token']
refresh_token = tokens['refresh_token']
tokens = refreshToken(tokens)

print('Similar users for testUserA: ', getSimilarUsers('testUserA', include_scores = True))
print('Similar users for testUserB: ', getSimilarUsers('testUserB', include_scores = True))
print('Similar users for testUserC: ', getSimilarUsers('testUserC', include_scores = True))
print('Similar users for testUserD: ', getSimilarUsers('testUserD', include_scores = True))

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
