import React, { Component } from 'react';
import { SpotifyAuth, Scopes } from 'react-spotify-auth'
import './App.css';
import Navbar from './components/Navbar';
import Profile from './components/pages/Profile';
import ShareMusic from './components/pages/ShareMusic';
import Feed from './components/pages/Feed';
import Notifications from './components/pages/Notifications';
import Callback from './components/Callback';
import SignIn from './components/pages/SignIn';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import Cookies from 'js-cookie';

// Create an axios instance that will be exported to use across pages.
// The interceptor below will be run on every request before it get sent,
//     setting the flask session workaround header to the proper value.
const axios_instance = require('axios');
axios_instance.interceptors.request.use((config) => {
	config.headers['X-Flask-Session-Workaround'] = Cookies.get('flask-session-workaround')
	return config
});
export const axios = axios_instance;

function App() {
  return (
    <>
    <Router>
      <Navbar />
        <Switch>
          <Route path='/' exact/>
          <Route path='/profile' component={Profile} />
          <Route path='/share-music' component={ShareMusic} />
          <Route path='/feed' component={Feed} />
          <Route path='/notifications' component={Notifications} />
          <Route path='/sign-in' component={SignIn} />
          <Route path='/callback' component={Callback}/>
        </Switch>
    </Router>
    </>
  );
}

export default App;