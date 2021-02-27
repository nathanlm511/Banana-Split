import React, { Component } from "react";
import { Link } from "react-router-dom";
import axios from 'axios';

import './Camera.css';

class Camera extends Component {
  constructor() {
    super();
    this.state = {}
    this.handleSubmit = this.handleSubmit.bind(this);
    this.fileInput = React.createRef();
  }

  useCamera() {
    console.log("hello");
  }

  handleSubmit(e) {
    //alert("test");
    const imageFile = this.fileInput.current.files[0];
    alert(imageFile);
    console.dir(imageFile);
    e.preventDefault();
  }

  render() {
    return (
      <div className="camera">
        <form onSubmit={this.handleSubmit} className="camera-form">
         <input type="file" accept="image/*" capture="camera" ref={this.fileInput}></input>
         <br></br>
          <input type="submit"/>
        </form>
      </div>
    );
  }
}
export default Camera;