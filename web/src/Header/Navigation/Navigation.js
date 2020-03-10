import React from 'react';
import './Navigation.css';
import {Link} from "react-router-dom";

function Navigation() {
    return (

        <nav>
            <ul>
                <li><Link to="/get">GET</Link></li>
                <li><Link to="/post">POST</Link></li>
                <li><Link to="/put">PUT</Link></li>
                <li><Link to="/delete">DELETE</Link></li>
            </ul>
        </nav>
    );
}

export default Navigation;
