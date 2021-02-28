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
    const userToken = JSON.parse(window.localStorage.getItem("token"))

    var formData = new FormData();
    formData.append('file', imageFile);
    axios.post("http://localhost:5000/test_image", formData)
    .then(res => {
      const userData = {items: res.data, username: userToken.username, num_users: 4, name: "Nathan's Reciept", host: userToken.phone};
      console.log(userData);
      axios.post("http://localhost:5000/create_session", userData)
      .then(res => {
        console.log(res.data);        
        window.localStorage.setItem("session_data", JSON.stringify(res.data[0]));        
        window.localStorage.setItem("session_id", JSON.stringify(res.data[0].id));
        window.location = "/list";
      })
      .catch(err => console.log(err));
    })
    .catch(err => console.log(err));
    e.preventDefault();
  }

  render() {
    return (
      <div className="camera">
        <div className="card">
          <form onSubmit={this.handleSubmit} className="camera-form">         
          <input type="file" accept="image/*" capture="camera" ref={this.fileInput} className="photo-input"></input>
          <br></br>
            <input type="submit" className="photo-submit"/>
          </form>
        </div>
      </div>
    );
  }
}
export default Camera;