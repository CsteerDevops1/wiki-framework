import React from 'react';
import './Navigation.css';
import {Link} from "react-router-dom";

function Navigation() {
    return (

        <nav>
            <ul>
                <li><Link to="/get">View all</Link></li>
                <li><Link to="/post">Add</Link></li>
                <li><Link to="/put">Edit</Link></li>
                <li><Link to="/delete">Delete</Link></li>
            </ul>
        </nav>
    );
}

export default Navigation;
