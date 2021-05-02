#
# Handles connecting to the last.fm api, allowing you to:
#
# 1) Get a list of songs that are similar to a user's liked songs.
#        getUserRankedSimilarSongs(user)
#
# 2) Get a list of ranked tags that describe a user's listening preferences.
#        getUserRankedTags(user)
#
# 3) Use the above to find "similar users" for things like friend recommendations.
#        getSimilarUsers(user, include_scores)
#

import itertools
import math
import os
import requests
import json

LAST_FM_API_KEY = os.environ.get("LAST_FM_API_KEY")

SIMILAR_TRACKS_URL = 'http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={1}&track={0}&api_key={2}&autocorrect=1&limit=3&format=json'
TOP_TAGS_URL = 'https://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={1}&track={0}&api_key={2}&format=json'
SIMILAR_TAGS_URL = 'http://ws.audioscrobbler.com/2.0/?method=tag.getsimilar&tag={0}&api_key={1}&format=json'

# == Last.FM API methods == #

def getSimilarTracks(song, artist):
	print("song: {}, artist: {}".format(song, artist))
	api_response = requests.get(SIMILAR_TRACKS_URL.format(song, artist, LAST_FM_API_KEY)).json()
	if 'similartracks' in api_response:
		return [song['name'] for song in api_response['similartracks']['track']]
	else:
		return None

def getTrackTopTags(song, artist):
	api_response = requests.get(TOP_TAGS_URL.format(song, artist, LAST_FM_API_KEY)).json()
	if 'toptags' in api_response:
		return api_response['toptags']['tag']
	else:
		return None


# == Methods to get the user's top X == #

def getUserRankedSongs(mongo, user):
	# This might want to be implemented in a way that takes the user's listening habits into account
	return getUserSongs(mongo, user)

def getUserRankedSimilarSongs(mongo, user, songs = None):
	if songs == None:
		songs = getUserSongs(user)
	unflattened_similar_songs = [x for x in [getSimilarTracks(mongo, song['title'], song['artist']) for song in songs] if x is not None]
	return list(dict.fromkeys(list(itertools.chain(*unflattened_similar_songs))))

def getUserRankedTags(mongo, user, songs = None):
	if songs == None:
		songs = getUserSongs(user)
	uncombined_tags = [getTrackTopTags(mongo, song['title'], song['artist']) for song in songs]
	tag_scores = {}
	for song_tags in uncombined_tags:
		if song_tags is None:
			continue
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

def getSimilarUsers(mongo, user, include_scores = False):
	# Can't get this info directly from Last.FM,
	# but can get track, similar tracks, and tag
	# info for a user's songs, then use that to 
	# determine how similar they are.
	# Step 1) Get data from Last.FM for the current user
	songs = getUserRankedSongs(mongo, user)
	similar_songs = getUserRankedSimilarSongs(mongo, user, songs=songs)
	tags = getUserRankedTags(mongo, user, songs=songs)
	# Step 2) Calculate similarity scores
	# TODO: Numbers might need to be tweaked
	similar_users = {}
	all_users = getAllUsers(mongo)
	for other_user in all_users:
		if other_user == user.user_id:
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

# == User function stubs == #

def getAllUsers(mongo):
    # return ['testUserA', 'testUserB', 'testUserC', 'testUserD']
	return mongo.db.users.distinct("id")

def getUserSongs(mongo, user):
    playlists_urls = list(mongo.db.playlists.aggregate([
        {
            "$match": {
                "id":user.user_id
            }
        }, 
        {
            "$unwind": "$playlists"
        }, 
        {
            "$group": {
                "_id": None, 
                "playlists": {
                    "$push": "$playlists.tracks.href"
                }
            }
        }, 
        {
            "$project": {
                "playlists": 1,
                "_id": 0
            }
        }
    ]))[0]['playlists']
    songs = []
    for playlist_url in playlists_urls:
        print("request url is {}".format("{}?market=US".format(playlist_url)))
        print("auth header is {}".format(user.authorization_header))
        response = requests.get("{}?market=US".format(playlist_url), headers=user.authorization_header).text
        print("response was {}".format(response))
        song_data = json.loads(response)
        print("song_data was {}".format(song_data))
        for item in song_data['items']:
            songs.append({'artist': item['track']['artists'][0]['name'], 'title': item['track']['name']})
    return songs

# == Test code == #
# print('Similar users for testUserA: ', getSimilarUsers('testUserA', include_scores = True))
# print('Similar users for testUserB: ', getSimilarUsers('testUserB', include_scores = True))
# print('Similar users for testUserC: ', getSimilarUsers('testUserC', include_scores = True))
# print('Similar users for testUserD: ', getSimilarUsers('testUserD', include_scores = True))



