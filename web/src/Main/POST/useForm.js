import {useState} from 'react';
import DatabaseModel from "../scheme/DatabaseModel";
import Attachment from '../scheme/Attachment';

function useForm(callback) {
 const [dbm, setDbm] = useState(new DatabaseModel());
  const handleSubmit = (event) => {
    if (event) {
        event.preventDefault();

        dbm["tags"] = [];
        dbm["synonyms"] = [];
        dbm["relations"] = []; 
        let globName = "188.124.37.185";
        let apiUrl = "/api/wiki";
        console.log(JSON.stringify(dbm));
        fetch("http://" + globName + ":5000" + apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dbm) // body data type must match "Content-Type" header
        }).then((data) => {console.log(data)});

    }
  }
  const handleInputChange = (event) => {
    event.persist();
    dbm[event.target.name] = event.target.value;
    setDbm(dbm);
  }

  const fileSelectedHandler = (event) => {
      dbm["attachments"] = [];
      console.log(event.target)
      console.log(event.target.files[0])
      console.log(event.target.files[0].type)

      const file = document.querySelector('input[type=file]').files[0];
      const reader = new FileReader();
      
      reader.addEventListener("load", function () {
         // here encoding to base64 happens
         console.log(reader.result)
        dbm.addAttachment(new Attachment(file.type, reader.result.replace(/data.*base64,/, "")));
        }, false);
      
      if (file) {
        reader.readAsDataURL(file);
      }
  }

  return {
    handleSubmit,
    handleInputChange,
    fileSelectedHandler,
    dbm
  };
}

export default useForm;