import {useState} from 'react';
import DatabaseModel from "../scheme/DatabaseModel";
import Attachment from '../scheme/Attachment';
import { useHistory } from "react-router-dom";

function useForm(callback) {
 const [dbm, setDbm] = useState(new DatabaseModel());
 let history = useHistory();

 const handleSubmit = (event) => {
    if (event) {
        event.preventDefault();
        if(event.target.name.value){dbm["name"] = event.target.name.value;}
        dbm["russian_name"] = event.target.russian_name.value;
        dbm["description"] = event.target.description.value;
        dbm["russian_description"] = event.target.russian_description.value;
        dbm["text"] = event.target.text.value;
        dbm["tags"] = [];
        dbm["synonyms"] = [];
        dbm["relations"] = []; 

        //here async file upload starts
        dbm["attachments"] = [];

        const file = document.querySelector('input[type=file]').files[0];
        const reader = new FileReader();
        reader.addEventListener("load", function () {
          // here encoding to base64 happens
          // we need to wait until file is ready and THEN we send data
          dbm.addAttachment(new Attachment(file.type, reader.result.replace(/data.*base64,/, "")));
          SendData();
        }, false);
       
        if (file) {
         reader.readAsDataURL(file);
        } else {
          SendData();
        }
    }
  };

  function SendData(){
    //just sends whatever is in dbm item
    let globName = "188.124.37.185";
    let apiUrl = "/api/wiki";

    fetch("http://" + globName + ":5000" + apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dbm) // body data type must match "Content-Type" header
    }).then((data) => {
      console.log(data.status);
      if([200,201,202,203,204,205].includes(data.status)){
      alert("Data sent successfully!");
      history.push('/get');} 
      else if([400,401,402,403,404,405].includes(data.status)){
      alert("Client error!");} 
      else if([500,501,502,503,504,505].includes(data.status)){
      alert("Server error!");}
      
  })}

  return {
    handleSubmit
  };
}

export default useForm;
