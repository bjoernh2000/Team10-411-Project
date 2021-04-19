'use strict';

require('./mongoose')();
var passport = require('passport');
var SpotifyStrategy = require('passport-spotify').Strategy;
var User = require('mongoose').model('User');
var config = require('./config');

module.exports = function () {

    passport.use(new SpotifyStrategy({
            clientID: config.spotifyAuth.clientID,
            clientSecret: config.spotifyAuth.clientSecret,
            callbackURL: 'http://localhost:3000/auth/spotify/callback',
        },
        function (accessToken, refreshToken, profile, done) {
            User.upsertSpotifyeUser(accessToken, refreshToken, profile, function(err, user) {
                return done(err, user);
            });
        }));
};