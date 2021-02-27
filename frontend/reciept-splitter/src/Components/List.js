import React, { Component } from "react";
import { Link } from "react-router-dom";
import axios from 'axios';

import './List.css';

class List extends Component {
  constructor() {
    super();
    this.state = {
      items: [{id: "1", name: "water", price: 14, percentage: 34, checked: false, slider: 0, otherPercentages: [12, 25, 30]},
                {id: "2", name: "milk", price: 24, percentage: 100, checked: false, slider: 0, otherPercentages: []},
                {id: "3", name: "grass", price: 9, percentage: 50, checked: false, slider: 0, otherPercentages: [50]}]
    }
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

  render() {
    return (
      <div className="list">
        <div className="reciept-container">
          {this.state.items.map((item) => {
            let leftTotal = item.percentage;
            return (
            <div key={item.id} className="item-container">
            <div className={item.checked ? 'check' : 'uncheck'} onClick={() => this.check(item.id)}/>
              <div className="item-box">    
                <input style={{width: item.percentage + "%"}} type="range" min="0" max="100" 
                  value={item.slider} onChange={(e) => this.handleSlider(e, item.id)} className={item.checked ? 'slider' : "no-slider"}/>  
                {item.otherPercentages.map((percent, index) => {
                  let tempLeft = leftTotal;
                  leftTotal += percent;
                  return <div className={"other-highlight-" + index} style={{left: tempLeft + "%", width: percent + "%"}}/>
                })}
                <div className="user-highlight" style={{width: (item.percentage * item.slider / 100) + "%"}}/>
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
      </div>
    );
  }
}
export default List;