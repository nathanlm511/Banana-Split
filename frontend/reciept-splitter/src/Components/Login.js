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
        /*
        axios.post("http://localhost:5000/get_session")
          .then(sessionData => {
            // window.location = 
          })
          .catch(err => console.log(err));
        */
        let session_id = window.localStorage.getItem("session_id");
        // {Name: "Sam", Items: [{Name: "Apple", ID: 1, price: 10, Percentage:}, {Name: "Bread", ID: 2, price: 15}]},
        const session_data = {
          name: "My Grocery List",
          host: "Nathan", 
          current_user: "",
          //current_user: {name: "Sam", items: [{name: "Apple", id: 1, price: 10, percentage: 17}, {name: "Bread", id: 2, price: 15, percentage: 36}],
            //            id: "7482", username: "Justv"},
          users: [
                  {name: "Justin", items: [{name: "Chai", id: 3, price: 8, percentage: 50}, {name: "Dates", id: 4, price: 6, percentage: 100}],
                   id: "7482", username: "Justv"},
                  {name: "Nathan", items: [{name: "Bread", id: 2, price: 15, percentage: 25}, {name: "Chai", id: 3, price: 8, percentage: 25}],
                  id: "0260", username: "NatM"}],
          items: [{name: "Apple", id: 1, price: 10},
                  {name: "Bread", id: 2, price: 15},
                  {name: "Chai", id: 3, price: 8},
                  {name: "Dates", id: 4, price: 6}]
        }

        window.localStorage.setItem("session_data", JSON.stringify(session_data));
        window.location = "/list";
      })
      .catch(err => console.log(err));
  }

  componentDidMount() {
    window.localStorage.setItem("session_id", window.location.href.split('\\').pop().split('/').pop());    
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