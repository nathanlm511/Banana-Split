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
    /*
    axios.post(url, data)
      .then(res => {
        window.localStorage.setItem("token", JSON.stringify());
        window.location = "/list"
      })
      .catch(err => alert(err))
    */
    alert("Username: " + this.state.username + "\nPassword: " + this.state.password)
    event.preventDefault();
    window.location = "/list";
  }

  render() {
    return (
      <div className="login">
        <div className="card">
          <form onSubmit={this.handleSubmit}>
            <label>
              Username:
              <input
                name="username"
                type="text"
                value={this.state.username}
                onChange={this.handleInputChange} />
            </label>
            <br />
            <label>
              Password:
              <input
                name="password"
                type="text"
                value={this.state.password}
                onChange={this.handleInputChange} />
            </label>
            <input type="submit" value="Submit" />
          </form>        
        </div>
      </div>
    );
  }
}
export default Login;