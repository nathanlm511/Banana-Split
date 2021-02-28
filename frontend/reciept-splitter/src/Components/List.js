import React, { Component } from "react";
import { Link } from "react-router-dom";
import axios from 'axios';

import './List.css';

class List extends Component {
  constructor() {
    super();
    /*
    this.state = {
      items: [{id: "1", name: "water", price: 14, percentage: 34, checked: false, slider: 0, otherPercentages: [12, 25, 30]},
                {id: "2", name: "milk", price: 24, percentage: 100, checked: false, slider: 0, otherPercentages: []},
                {id: "3", name: "grass", price: 9, percentage: 50, checked: false, slider: 0, otherPercentages: [50]}]
    
    }
    */
   this.confirm = this.confirm.bind(this);
  }

  componentWillMount() {
    const session_data = JSON.parse(window.localStorage.getItem("session_data"));
    const user_token = JSON.parse(window.localStorage.getItem("token"));
    if (session_data.cuurent_user == "") {
      // already done
    }
    else {
      // current user 
    }
    let users = [];
    let items = [];
    let index = 0;
    users.push({name: user_token.username, id: user_token.id, num: index});
    index++;
    session_data.users.forEach(user => {
      users.push({name: user.username, id: user.id, num: index});
      index++;
    });
    session_data.items.forEach(item => {
      let newItem = item;
      newItem.checked = false;
      newItem.slider = 0;
      newItem.otherPercentages = [];
      items.push(newItem);
    });
    if (!session_data.current_user == "") {
      session_data.current_user.items.forEach(item => {
        let item_matched = items.find(e => e.id == item.id);
        item_matched.slider = item.percentage;
        item_matched.checked = true;
      });
    }
    index = 1;
    session_data.users.forEach(user => {
      user.items.forEach(item => {
        let item_matched = items.find(e => e.id == item.id);
        item_matched.otherPercentages.push({id: index, percentage: item.percentage});
      });
      index++;
    });    
    items.forEach(item => {
      let percentageSum = 0;
      item.otherPercentages.forEach(percentage => percentageSum += percentage.percentage);
      item.percentage = 100 - percentageSum;
    });
    this.setState({items:items, users: users});
  }

  check(id) {
    let newItems = this.state.items.slice();
    let i = newItems.findIndex(item => {
      return item.id == id;
    });
    let currentItem = newItems[i];

    if (currentItem.checked) {
      currentItem.checked = false;
      currentItem.slider = 0;
    }
    else {
      currentItem.checked = true;  
      currentItem.slider = 100;
    }
    this.setState({items: newItems});
  }

  handleSlider(e, id) {
    let newItems = this.state.items.slice();
    let i = newItems.findIndex(item => {
      return item.id == id;
    });
    newItems[i].slider = e.target.value;
    this.setState({items: newItems});
  }

  confirm() {
    let itemsToDb = [];
    this.state.items.forEach(item => {
      let newItem = {};
      newItem.id = item.id;
      newItem.name = item.name;
      newItem.price = item.price;
      newItem.percentage = item.slider * item.percentage;
      itemsToDb.push(newItem);
    });
    const user_token = JSON.parse(window.localStorage.getItem("token"));
    let current_user = {};
    current_user.name = user_token.username;
    current_user.id = user_token.id;
    current_user.items = itemsToDb;
  }

  render() {
    // check if user is authenticated
    if (!window.localStorage.getItem("token")) {
      console.log("user not authenticated");
      window.location = '/';
    }
    return (
      <div className="list">
        <div className="legend-container">
          {this.state.users.map((user) => {
            return (
            <div key={user.id} className="user-container">
              <div>{user.name}</div>
              <div className={"highlight-" + user.num + " circle"}></div>
            </div>
            )            
          })}
        </div>
        <div className="legend-whitespace" />
        <div className="reciept-container">
          {this.state.items.map((item) => {
            let leftTotal = item.percentage;
            let index = 0;
            return (
            <div key={item.id} className="item-container">
            <div className={item.checked ? 'check' : 'uncheck'} onClick={() => this.check(item.id)}/>
              <div className="item-box">    
                <input style={{width: item.percentage + "%"}} type="range" min="0" max="100" 
                  value={item.slider} onChange={(e) => this.handleSlider(e, item.id)} className={item.checked ? 'slider' : "no-slider"}/>  
                {item.otherPercentages.map((percent) => {
                  let tempLeft = leftTotal;
                  leftTotal += percent.percentage;
                  index++;
                  return <div className={"other-highlight highlight-" + percent.id} style={{left: tempLeft + "%", width: percent.percentage + "%"}}/>
                })}
                <div className="user-highlight highlight-0" style={{width: (item.percentage * item.slider / 100) + "%"}}/>
                <div>
                  {item.name}
                </div>
                <div>
                  {item.price}
                </div>
              </div>
              <div>
                {Math.round(item.slider * item.percentage / 100)} %
              </div>
            </div>             
          )})}            
        </div>
        <div>
          {(this.state.items.reduce((accumulator, item) => (accumulator) + (item.price * item.slider / 100), this.state.items[0].price * this.state.items[0].slider / 100)).toFixed(2)}
        </div>
        <div className="confirm-button" onClick={this.confirm}>
          CONFIRM
        </div>
      </div>
    );
  }
}
export default List;