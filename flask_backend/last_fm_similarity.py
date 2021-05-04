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

def getSimilarTracks(mongo, song, artist):
    print("song: {}, artist: {}".format(song, artist))
    cached = mongo.db.cache.find({"api":"last.fm","endpoint":"similar_tracks","song":song,"artist":artist})
    if cached.count() > 0:
        api_response = cached[0]["api_response"]
    else:
        api_response = requests.get(SIMILAR_TRACKS_URL.format(song, artist, LAST_FM_API_KEY)).json()
        mongo.db.cache.insert({"api":"last.fm","endpoint":"similar_tracks","song":song,"artist":artist,"api_response":api_response})
    if 'similartracks' in api_response:
        return [song['name'] for song in api_response['similartracks']['track']]
    else:
        return None

def getTrackTopTags(mongo, song, artist):
    cached = mongo.db.cache.find({"api":"last.fm","endpoint":"top_tags","song":song,"artist":artist})
    if cached.count() > 0:
        api_response = cached[0]["api_response"]
    else:
        api_response = requests.get(TOP_TAGS_URL.format(song, artist, LAST_FM_API_KEY))
        try:
            api_response = api_response.json()
            mongo.db.cache.insert({"api":"last.fm","endpoint":"top_tags","song":song,"artist":artist,"api_response":api_response})
        except:
            return None
    if 'toptags' in api_response:
        return api_response['toptags']['tag']
    else:
        return None


# == Methods to get the user's top X == #

def getUserRankedSongs(mongo, authorization_header, user_id, allow_private_playlists = False):
    # This might want to be implemented in a way that takes the user's listening habits into account
    return getUserSongs(mongo, user_id, authorization_header, allow_private_playlists)

def getUserRankedSimilarSongs(mongo, user_id, authorization_header, songs = None, allow_private_playlists = False):
    if songs == None:
        songs = getUserSongs(mongo, user_id, authorization_header, allow_private_playlists)
    unflattened_similar_songs = [x for x in [getSimilarTracks(mongo, song['title'], song['artist']) for song in songs] if x is not None]
    return list(dict.fromkeys(list(itertools.chain(*unflattened_similar_songs))))

def getUserRankedTags(mongo, user_id, authorization_header, songs = None, allow_private_playlists = False):
    if songs == None:
        songs = getUserSongs(mongo, user_id, authorization_header, allow_private_playlists)
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
    songs = getUserRankedSongs(mongo, user.authorization_header, user.user_id, allow_private_playlists=True)
    similar_songs = getUserRankedSimilarSongs(mongo, user.user_id, user.authorization_header, songs=songs, allow_private_playlists=True)
    tags = getUserRankedTags(mongo, user.user_id, user.authorization_header, songs=songs, allow_private_playlists=True)
    # Step 2) Calculate similarity scores
    # TODO: Numbers might need to be tweaked
    similar_users = {}
    all_users = getAllUsers(mongo)
    for other_user in all_users:
        if other_user == user.user_id:
            continue
        # This data should *really* be stored in the database so this isn't hitting the Last.FM API so many times per recommendation
        other_user_songs = getUserRankedSongs(mongo, user.authorization_header, other_user, allow_private_playlists=False)
        other_user_tags = getUserRankedTags(mongo, other_user, user.authorization_header, allow_private_playlists=False)
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

def getUserSongs(mongo, user_id, authorization_header, allow_private_playlists):
    print("get songs for {}".format(user_id))
    playlists_urls = list(mongo.db.playlists.aggregate([
        {
            "$match": {
                "id":user_id
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
        print("  reading songs for playlist {}".format("{}?market=US".format(playlist_url)))
        cached = mongo.db.cache.find({"api":"spotify","endpoint":"playlist_tracks","url":playlist_url,"allow_private":allow_private_playlists})
        if cached.count() > 0:
            response = cached[0]["api_response"]
        else:
            response = requests.get("{}?market=US".format(playlist_url), headers=authorization_header).text
            mongo.db.cache.insert({"api":"spotify","endpoint":"playlist_tracks","url":playlist_url,"allow_private":allow_private_playlists,"api_response":response})
        song_data = json.loads(response)
        for item in song_data['items']:
            if item is not None and item['track'] is not None and item['track']['artists'] is not None and item['track']['artists'][0] is not None:
                songs.append({'artist': item['track']['artists'][0]['name'], 'title': item['track']['name']})
                print("    found song {} - {}".format(item['track']['name'], item['track']['artists'][0]['name']))
    return songs

# == Test code == #
# print('Similar users for testUserA: ', getSimilarUsers('testUserA', include_scores = True))
# print('Similar users for testUserB: ', getSimilarUsers('testUserB', include_scores = True))
# print('Similar users for testUserC: ', getSimilarUsers('testUserC', include_scores = True))
# print('Similar users for testUserD: ', getSimilarUsers('testUserD', include_scores = True))



