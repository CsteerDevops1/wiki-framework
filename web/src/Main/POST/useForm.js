import React, {useState} from 'react';
import DatabaseModel from "../scheme/DatabaseModel";
import Attachment from '../scheme/Attachment';
import { useHistory } from "react-router-dom";
import ReactDOM from "react-dom";

function useForm(callback) {
 const [dbm] = useState(new DatabaseModel());
 let history = useHistory();
 dbm["attachments"] = [];

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

        //just sends whatever is in dbm item
        let globName = "188.124.37.185";
        let apiUrl = "/api/wiki";

        fetch("https://" + globName + apiUrl, {
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
        })
        }
  };
    
  const handleFileSelect = (event) => {
    const file =  event.target.files[0];
    if(/image.*/.test(file.type)){
      ReactDOM.render(<img alt="" src = { URL.createObjectURL(file) } width="300" height="300"/>, document.getElementById("preview").appendChild(document.createElement('div')));
    } else if(/audio.*/.test(file.type)){
      ReactDOM.render(<audio controls src={URL.createObjectURL(file)} width="300" height="300"/>, document.getElementById("preview").appendChild(document.createElement('div')))
    } else if (/video.*/.test(file.type)){
      ReactDOM.render(<video controls src={URL.createObjectURL(file)} width="300" height="300"/>, document.getElementById("preview").appendChild(document.createElement('div')))
    } else {
      ReactDOM.render(<a href={URL.createObjectURL(file)} >{file.name}</a>, document.getElementById("preview").appendChild(document.createElement('div')))
    }

    const reader = new FileReader();
    reader.addEventListener("load", function () {
          // here encoding to base64 happens
          // we need to wait until file is ready and THEN we send data
          dbm.addAttachment(new Attachment(file.type, reader.result.replace(/data.*base64,/, "")));
          console.log("file added");
    }, false);
       
    if (file) {
      reader.readAsDataURL(file);
    } 
  }
  
  return {
    handleSubmit,
    handleFileSelect
  };
}

export default useForm;
