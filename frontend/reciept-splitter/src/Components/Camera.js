import React, { Component } from "react";
import { Link } from "react-router-dom";
import axios from 'axios';

import './Camera.css';

class Camera extends Component {
  constructor() {
    super();
    this.state = {}
    this.handleSubmit = this.handleSubmit.bind(this);
    this.updateFileName = this.updateFileName.bind(this);
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
      console.log("-------");
      console.log(res.data);
      const userData = {items: res.data, username: userToken.username, num_users: 4, name: "Nathan's Reciept", host: userToken.phone};
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

  updateFileName() {
    if (this.fileInput.current && this.fileInput.current.files && this.fileInput.current.files[0]) {
      this.setState({filename: this.fileInput.current.files[0].name});      
    }
  }

  render() {
    return (
      <div className="camera">
        <div className="camera-title">
          Take a picture of the receipt!
        </div>
        <div className="photo-container">
          <div className="receipt"/>
          <div className="camera-pic"/>
          <div className="bananya"/>
        </div>
        <div className="card">
          <div className="instructions">
            Let the AI do all the work for you! Using techniques such as feature extracting, pruning, homography transformations, and OCR, we'll read the reciept so you don't have to!
          </div>
          <form onSubmit={this.handleSubmit} className="camera-form">   
          <div className='file-input'>
            <input id="photo-id" type="file" accept="image/*" capture="camera" ref={this.fileInput} className="photo-input" onChange={this.updateFileName}></input>
            <span className='button'>Choose</span>
            <label className='label'>{this.state.filename ? this.state.filename : "No file chosen"}</label>
          </div>     
          
          <br></br>
            <input type="submit" className="photo-submit" value="Magic!"/>
          </form>
        </div>
      </div>
    );
  }
}
export default Camera;