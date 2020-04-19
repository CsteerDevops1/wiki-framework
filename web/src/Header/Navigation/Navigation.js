import React from 'react';
import './Navigation.css';
import {Link} from "react-router-dom";

function Navigation() {
    return (

        <nav>
            <ul>
                <li><Link to="/get">View all</Link></li>
                <li><Link to="/post">Create new</Link></li>
            </ul>
        </nav>
    );
}

export default Navigation;
