#
# Handles connecting to the last.fm api, allowing you to:
#
# 1) Get a list of songs that are similar to a user's liked songs.
#        getUserRankedSimilarSongs(mongo, user_id, authorization_header, allow_private_playlists = False)
#
# 2) Get a list of ranked tags that describe a user's listening preferences.
#        getUserRankedTags(mongo, user_id, authorization_header, songs = None, allow_private_playlists = False)
#
# 3) Use the above to find "similar users" for things like friend recommendations.
#        getSimilarUsers(mongo, user, include_scores = False)
#

import itertools
import math
import os
import requests
import random
import json

app_config = json.load(open('../frontend/src/config.json',))
LAST_FM_API_KEY = app_config["LAST_FM_API_KEY"]

SIMILAR_TRACKS_URL = 'http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={1}&track={0}&api_key={2}&autocorrect=1&limit=3&format=json'
TOP_TAGS_URL = 'https://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={1}&track={0}&api_key={2}&format=json'
SIMILAR_TAGS_URL = 'http://ws.audioscrobbler.com/2.0/?method=tag.getsimilar&tag={0}&api_key={1}&format=json'

# == Last.FM API methods == #

def getSimilarTracks(mongo, song, artist, only_use_cached_data):
    # print("song: {}, artist: {}".format(song, artist))
    cached = mongo.db.cache.find({"api":"last.fm","endpoint":"similar_tracks","song":song,"artist":artist})
    api_response = []
    if cached.count() > 0:
        api_response = cached[0]["api_response"]
    elif not only_use_cached_data:
        try:
            api_response = requests.get(SIMILAR_TRACKS_URL.format(song, artist, LAST_FM_API_KEY)).json()
            mongo.db.cache.insert({"api":"last.fm","endpoint":"similar_tracks","song":song,"artist":artist,"api_response":api_response})
        except:
            return None
    if 'similartracks' in api_response:
        return [song['name'] for song in api_response['similartracks']['track']]
    else:
        return None

def getTrackTopTags(mongo, song, artist, only_use_cached_data):
    cached = mongo.db.cache.find({"api":"last.fm","endpoint":"top_tags","song":song,"artist":artist})
    api_response = []
    if cached.count() > 0:
        api_response = cached[0]["api_response"]
    elif not only_use_cached_data:
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

def getUserRankedSongs(mongo, user_id, authorization_header, only_use_cached_data, allow_private_playlists = False):
    # This should be implemented in a way that takes the user's listening habits into account
    user_songs = getUserSongs(mongo, user_id, authorization_header, only_use_cached_data, allow_private_playlists)
    random.shuffle(user_songs)
    return user_songs

def getUserRankedSimilarSongs(mongo, user_id, authorization_header, only_use_cached_data, songs = None, allow_private_playlists = False):
    cached = mongo.db.cache.find({"api":"internal", "endpoint":"user_ranked_similar_songs", "allow_private": allow_private_playlists, "wipe_on_login":user_id})
    if cached.count() > 0:
        return cached[0]["api_response"]
    if songs == None:
        songs = getUserSongs(mongo, user_id, authorization_header, only_use_cached_data, allow_private_playlists)
    unflattened_similar_songs = [x for x in [getSimilarTracks(mongo, song['title'], song['artist'], only_use_cached_data) for song in songs] if x is not None]
    ranked_simliar_songs = list(dict.fromkeys(list(itertools.chain(*unflattened_similar_songs))));
    if not only_use_cached_data:
        mongo.db.cache.insert({"api":"internal", "endpoint":"user_ranked_similar_songs", "allow_private": allow_private_playlists, "wipe_on_login":user_id, "api_response": ranked_simliar_songs})
    return ranked_simliar_songs

def getUserRankedTags(mongo, user_id, authorization_header, only_use_cached_data, songs = None, allow_private_playlists = False):
    cached = mongo.db.cache.find({"api":"internal", "endpoint":"used_ranked_tags", "allow_private": allow_private_playlists, "wipe_on_login":user_id})
    if cached.count() > 0:
        return cached[0]["api_response"]
    if songs == None:
        songs = getUserSongs(mongo, user_id, authorization_header, only_use_cached_data, allow_private_playlists)
    uncombined_tags = [getTrackTopTags(mongo, song['title'], song['artist'], only_use_cached_data) for song in songs]
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
    if not only_use_cached_data:
        mongo.db.cache.insert({"api":"internal", "endpoint":"used_ranked_tags", "allow_private": allow_private_playlists, "wipe_on_login":user_id, "api_response": tags})
    return tags

# == Friend recommendations == #

def getSimilarUsers(mongo, user, include_scores = False, only_use_cached_data = False):

    # Can't get this info directly from Last.FM,
    # but can get track, similar tracks, and tag
    # info for a user's songs, then use that to 
    # determine how similar they are.
    
    # Step 1) Get data from Last.FM for the current user
    songs = getUserRankedSongs(mongo, user.user_id, user.authorization_header, only_use_cached_data, allow_private_playlists=True)
    similar_songs = getUserRankedSimilarSongs(mongo, user.user_id, user.authorization_header, only_use_cached_data, songs=songs, allow_private_playlists=True)
    tags = getUserRankedTags(mongo, user.user_id, user.authorization_header, only_use_cached_data, songs=songs, allow_private_playlists=True)
    
    # Step 2) Calculate similarity scores (iterate over all other users)
    similar_users = {}
    all_users = getAllUsers(mongo)
    for other_user in all_users:
        
        # No point calculating the user's similarity with themselves, it will always = 1.
        if other_user == user.user_id:
            continue
        
        # Step 2.1) Get the data from Last.FM for the other user
        # Note: We need to use the currently logged-in user's Spotify authorization header here, meaning we can't scan other user's private playlists,
        #       although in my mind this is the desired behavior anyway.
        other_user_songs = getUserRankedSongs(mongo, other_user, user.authorization_header, only_use_cached_data, allow_private_playlists=False)
        other_user_similar_songs = getUserRankedSimilarSongs(mongo, other_user, user.authorization_header, only_use_cached_data, songs=other_user_songs, allow_private_playlists=False)
        other_user_tags = getUserRankedTags(mongo, other_user, user.authorization_header, only_use_cached_data, songs=other_user_songs, allow_private_playlists=False)
        
        # Step 2.2) Use the rankedListSimilarity function from below to calculate a similarity score between the user and this other user
        similarity_score = 0.20 * rankedListSimilarity(songs, other_user_songs) + 0.40 * rankedListSimilarity(similar_songs, other_user_similar_songs) + 0.40 * rankedListSimilarity(tags, other_user_tags)
        
        similar_users[other_user] = similarity_score
    
    # Step 3) Format values and return
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
    if a is None or b is None:
        return 0.0
    print("rLS {} {}".format(len(a), len(b)))
    for i in range(len(a)):
        val = a[i]
        if val not in b:
            continue
        j = b.index(val)
        similarity += math.sqrt((len(a)-i)/float(len(a))*(len(b)-j)/float(len(b)))
    return similarity / max(1.0,float(len(a)))

# == User functions == #

def getAllUsers(mongo):
    return mongo.db.users.distinct("id")

def getUserSongs(mongo, user_id, authorization_header, only_use_cached_data, allow_private_playlists):

    cached = mongo.db.cache.find({"api":"internal", "endpoint":"all_user_songs", "allow_private": allow_private_playlists, "wipe_on_login":user_id})
    if cached.count() > 0:
        return cached[0]["api_response"]
        
    songs = []
    
    print("get liked songs for {}".format(user_id))
    liked_songs = mongo.db.liked_songs.find({"id":user_id})
    if "liked_songs" in liked_songs:
        for item in list(liked_songs["liked_songs"]):
            if item is not None and item['track'] is not None and item['track']['artists'] is not None and item['track']['artists'][0] is not None:
                songs.append({'artist': item['track']['artists'][0]['name'], 'title': item['track']['name']})
                print("  found liked song {} - {}".format(item['track']['name'], item['track']['artists'][0]['name']))
    
    print("get playlist songs for {}".format(user_id))

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
    ]))

    if (len(playlists_urls) == 0):
        return songs
    else:
        playlists_urls = playlists_urls[0]['playlists']
    
    for playlist_url in playlists_urls:
    
        # print("  reading songs for playlist {}".format("{}?market=US".format(playlist_url)))
        song_data = []
        
        request_url = "{}?market=US".format(playlist_url)
        while request_url is not None:
            cached = mongo.db.cache.find({"api":"spotify","endpoint":"playlist_tracks","url":request_url,"allow_private":allow_private_playlists})
            song_data_partial = []
            if cached.count() > 0:
                song_data_partial = json.loads(cached[0]["api_response"])
            elif not only_use_cached_data:
                response = requests.get(request_url, headers=authorization_header)
                mongo.db.cache.insert({"api":"spotify","endpoint":"playlist_tracks","wipe_on_login":user_id,"url":playlist_url,"allow_private":allow_private_playlists,"api_response":response.text})
                song_data_partial = json.loads(response.text)
            if "items" in song_data_partial:
                song_data.extend([x for x in song_data_partial["items"]])
            if "next" in song_data_partial:
                request_url = song_data_partial["next"]
            else:
                request_url = None
                
        
        for item in song_data:
            if item is not None and item['track'] is not None and item['track']['artists'] is not None and item['track']['artists'][0] is not None:
                songs.append({'artist': item['track']['artists'][0]['name'], 'title': item['track']['name']})
                # print("    found song {} - {}".format(item['track']['name'], item['track']['artists'][0]['name']))
    
    if not only_use_cached_data:
        mongo.db.cache.insert({"api":"internal", "endpoint":"all_user_songs", "allow_private": allow_private_playlists, "wipe_on_login":user_id, "api_response": songs})
    return songs
