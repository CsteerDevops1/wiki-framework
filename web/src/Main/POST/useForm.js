import {useState} from 'react';
import DatabaseModel from "../scheme/DatabaseModel";

function useForm(callback) {
 const [dbm, setDbm] = useState(new DatabaseModel());
  const handleSubmit = (event) => {
    if (event) {
        event.preventDefault();

        dbm["tags"] = [];
        dbm["synonyms"] = [];
        dbm["relations"] = [];
        dbm["attachments"] = [];

        let globName = "188.124.37.185";
        let apiUrl = "/api/wiki";
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
  return {
    handleSubmit,
    handleInputChange,
    dbm
  };
}

export default useForm;