import React from 'react';
import './Header.css';
import Navigation from "./Navigation/Navigation";
import {Link} from "react-router-dom";

function Header() {
  return (
      <header>
          <Link to="/">WikiFramework</Link>
          <Navigation/>
      </header>
  );
}

export default Header;
