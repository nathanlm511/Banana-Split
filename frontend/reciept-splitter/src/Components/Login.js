import React, { Component } from "react";
import { Link } from "react-router-dom";
import axios from 'axios';

import './Login.css';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: ""
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange(event) {
    const target = event.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  handleSubmit(event) {   
    event.preventDefault();
    axios.post("http://localhost:5000/host_login", 
    {username: this.state.username,
      password: this.state.password})
      .then(res => {
        window.localStorage.setItem("token", JSON.stringify(res.data));
        let session_id = window.localStorage.getItem("session_id");
        axios.post("http://localhost:5000/get_session", {id: session_id})
          .then(res => {
            console.log(res.data);
            window.localStorage.setItem("session_data", JSON.stringify(res.data[0]));
            window.location = "/list";
          })
          .catch(err => console.log(err));
      })
      .catch(err => console.log(err));
  }

  componentDidMount() {
    window.localStorage.setItem("session_id", window.location.href.split('\\').pop().split('/').pop());    
  }

  render() {
    return (
      <div className="login">
        <div className="title">
          <div className="title-intro">Welcome to</div>
          <div className="title-body-container">
            <div className="title-body"><span style={{"fontWeight": 400}}>Banana</span> Split</div>
            <div className="title-image"/>
          </div>
        </div>
        <div className="card">
          <div className="login-title">Authenticate with Venmo:</div>
          <form onSubmit={this.handleSubmit}>
            <div className="username-container">
              <div className="label">
                Username: 
              </div>
              <div className="field">
                <input
                    className="username-box"
                    name="username"
                    type="text"
                    value={this.state.username}
                    onChange={this.handleInputChange} 
                    autoComplete="off"/>
              </div>
            </div>  
            <br></br>
            <div className="password-container">
              <div className="label">
                Password: 
              </div>   
              <div className="field">
                <input
                  className="password-box"
                  name="password"
                  type="text"
                  value={this.state.password}
                  onChange={this.handleInputChange} 
                  autoComplete="off"/>
                </div>       
            </div>   
            <br></br> 
            <div className="login-button-row" >
              <input type="submit" value="Login" className="login-button"/>
            </div>  
          </form>        
        </div>
      </div>
    );
  }
}
export default Login;