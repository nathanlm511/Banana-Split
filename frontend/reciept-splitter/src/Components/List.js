import React, { Component } from "react";
import { Link } from "react-router-dom";
import axios from 'axios';

import './List.css';

class List extends Component {
  constructor() {
    super();
    this.state = {}
  }

  render() {
    return (
      <div className="list">
        <div className="reciept-container">
          <div className="item-container">
            Chicken
          </div>
          <div className="item-container">
            Eggs
          </div>
          <div className="item-container">
            Water
          </div>
        </div>
      </div>
    );
  }
}
export default List;