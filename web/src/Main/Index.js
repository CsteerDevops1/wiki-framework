import React from 'react';
import './Main.css';
import {Link} from "react-router-dom";

function Index() {
  return (
      <main>
        <h1>Hello! This is wiki home page. <br/></h1>
        <div>From here you can  <Link to="/get">view all</Link> wiki elements, <Link to="/post">create</Link> a new element or <Link to="/put">edit</Link> existing one.</div>
      </main>
  );
}

export default Index;
