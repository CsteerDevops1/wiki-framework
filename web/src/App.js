import React from 'react';
import './App.css';
import Footer from "./Footer/Footer";
import Header from "./Header/Header";
import Index from "./Main/Index";
import {
    BrowserRouter as Router,
    Switch,
    Route
} from "react-router-dom";
import GetPage from "./Main/GET/GetPage";
import PostPage from "./Main/POST/PostPage";
import PutPage from "./Main/PUT/PutPage";
import DeletePage from "./Main/DELETE/DeletePage";

function App() {
    return (
        <div id="App">
            <Router>
                <Header/>
                <Switch>
                    <Route exact path="/">
                        <Index/>
                    </Route>
                    <Route path="/get">
                        <GetPage/>
                    </Route>
                    <Route path="/post">
                        <PostPage/>
                    </Route>
                    <Route path="/put/:id">
                        <PutPage/>
                    </Route>
                     <Route path="/put">
                        <PutPage/>
                    </Route>
                     <Route path="/delete">
                        <DeletePage/>
                    </Route>
                </Switch>
            </Router>
            <Footer/>
        </div>
    );
}

export default App;
