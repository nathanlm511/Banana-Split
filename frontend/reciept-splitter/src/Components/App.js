import React, { Component } from 'react';

import Login from './Login';
import Camera from './Camera';
import List from './List';

import {Route} from 'react-router-dom'

import './App.css';

class App extends Component {

  // here is our UI
  // it is easy to understand their functions when you
  // see them render into our screen
  render() {
    return (
      <div className="app">
        <Route path="/login" component={Login} />
        <Route path="/camera" component={Camera} />
        <Route path="/list" component={List} />
        <Route exact path="/" component={Login} />
      </div>
    );
  }
}

export default App;
