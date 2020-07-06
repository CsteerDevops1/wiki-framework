import  {useState} from 'react';
import DatabaseModel from "../scheme/DatabaseModel";
import '../Main.css';

require('dotenv').config();
let hostName = process.env.REACT_APP_HOSTNAME;
let apiPath = "/api/wiki";

function getObjects(response) {
  if (Number(response.length) !== 0) {
      let dbObjects = [];
      response.forEach((element) => {
          dbObjects.push(DatabaseModel.parseObject(element))
      });
      return dbObjects;
  } else {
      return [];
  }
}

function useForm(callback) {
 let [models, setModels] = useState(null);
 const handleSubmit = (event) => {
    if (event) {
        event.preventDefault();
        models = null;
            if (!models) {
                // here we should pass search params
                fetch(hostName + apiPath + `?access_token=${sessionStorage.getItem('token')}&name=${event.target.name.value}`) 
                    .then(response => response.json())
                    .then(response => getObjects(response))
                    .then(data => setModels(data));
            }
      }
  };
  return {
    handleSubmit,
    models
  };
}

export default useForm;

  
  