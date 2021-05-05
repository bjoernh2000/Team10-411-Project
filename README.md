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
APIs work together in order to understand general trends in music taste, as
well as personal (single user) preferences.

## How to Run

In order to run BadDJ:
1. Install dependency programs
    * MongoDB
    * `npm`
2. `cd` into `flask_backend` and run `python app.py` for the backend server
3. In a second terminal,
    * `cd` into `frontend_ver2`
    * Run `npm install` to grab all `npm` dependencies 
    * `npm start` the frontend server
4. In a third terminal, start MongoDB with `mongod --dbpath <database_path>`
5. Open a web browser and navigate to `localhost:3000`