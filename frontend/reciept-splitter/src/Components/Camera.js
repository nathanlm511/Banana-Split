import React, { Component } from "react";
import { Link } from "react-router-dom";
import axios from 'axios';

import './Camera.css';

class Camera extends Component {
  constructor() {
    super();
    this.state = {}
  }

  useCamera() {
    console.log("hello");
  }

  render() {
    return (
      <div className="camera">
         <input type="file" accept="image/*" capture="camera" className="camera-button"></input>
        <div onClick={this.useCamera} className="camera-button">
          Take a Picture
        </div>
      </div>
    );
  }
}
export default Camera;