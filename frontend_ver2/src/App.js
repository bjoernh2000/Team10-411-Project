import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Profile from './components/pages/Profile';
import ShareMusic from './components/pages/ShareMusic';
import Feed from './components/pages/Feed';
import Notifications from './components/pages/Notifications';
import Callback from './components/Callback';
import SignIn from './components/pages/SignIn';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

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