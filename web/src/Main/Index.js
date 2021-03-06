import React, {useState, useEffect} from 'react';
import './Main.css';
import {getObjects} from "./GET/GetPage";
import {Link} from "react-router-dom";
import ModelElement from './items/ModelElement';

require('dotenv').config();
//getting hostname from web/.env
let hostName = process.env.REACT_APP_HOSTNAME;
let apiPath = "/api/wiki";
sessionStorage.setItem('token', localStorage.getItem('token')); 
console.log("token = " + sessionStorage.getItem('token'));

const randomArticles = (articles) => {
    const array = [...articles];
    const shuffleArray = (array) => {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
 
    shuffleArray(array);
    return array;
}

function Index() {
    const [models, setModels] = useState(null);
    useEffect(() => {
        if (!models) {
            fetch(hostName + apiPath + `?access_token=${sessionStorage.getItem('token')}&limit=10`)
                .then(response => response.json())
                .then(response => getObjects(response))
                .then(data => {
                    const articles = randomArticles(data);
                    setModels(articles)
                });
        }
    }, [models]);
 


  return (
      <main>
        <h1>Hello! This is wiki home page. <br/></h1>
        {((sessionStorage.getItem('token') === "null") || (sessionStorage.getItem('token') === null) ) &&
            <h1><a className="link" href="/login">Log in</a></h1> 
        }
        <div>From here you can  <Link className="link" to="/get">view all</Link> wiki elements, <Link className="link" to="/post">create</Link> a new element or <Link className="link" to="/put">edit</Link> existing one.</div>
        <div>Our bots:</div>
          <ul>
              <li><a className="link" href="https://t.me/cs_wiki_edit_bot">Edit bot</a></li>
              <li><a className="link" href="https://t.me/cs_wiki_media_bot">Media bot</a></li>
              <li><a className="link" href="https://t.me/cs_wiki_search_bot">Search bot</a></li>
              
          </ul>

          <ul>
              {(models != null) && models.map(item => <li key={item._id}>
                      <ModelElement
                          visibleFields={[
                              "name",
                              "russian_description",
                              "description",
                              "media"
                          ]}
 
                          isButtonVisible={false}
                          model={item}/>
                  </li>
              )}
          </ul>
      </main>
  );
}
 
export default Index;
