import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Profile from './components/pages/Profile';
import ShareMusic from './components/pages/ShareMusic';
import Discover from './components/pages/Discover';
import Notifications from './components/pages/Notifications';
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
          <Route path='/discover' component={Discover} />
          <Route path='/notifications' component={Notifications} />
        </Switch>
    </Router>
    </>
  );
}

export default App;
