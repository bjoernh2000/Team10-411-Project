# 411 Project: Music Sharing Platform ­— BadDJ

This is a music sharing space which users log into with Spotify.

Every person on this platform has some playlist that represents them on their
profile, and the app can suggest songs and other users with similar
preferences. People can also create conversations (like tweets with a
song/playlist/artist attached) to communicate with other users about
interests.

We use the Spotify API (https://developer.spotify.com/documentation/web-api/)
to get information about a person's genre/artist preferences to curate
appropriate user playlists. We use the last.fm API (https://www.last.fm/api) to
gather data about popular artists as it applies to people in general. The two
APIs work together in order to understand general trends in music taste,
as well as personal (single user) preferences.