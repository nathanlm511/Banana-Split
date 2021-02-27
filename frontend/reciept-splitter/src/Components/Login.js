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
        window.location = "/list"
      })
      .catch(err => console.log(err))
  }

  render() {
    return (
      <div className="login">
        <div className="card">
          <form onSubmit={this.handleSubmit}>
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
            <br></br>    
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