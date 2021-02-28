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
    var formData = new FormData();
    formData.append('file', imageFile);
    axios.post("http://localhost:5000/test_image", formData)
    .then(data => {

    })
    .catch(err => console.log(err));
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