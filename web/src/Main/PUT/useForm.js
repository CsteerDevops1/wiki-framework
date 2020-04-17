import {useState} from 'react';
import DatabaseModel from "../scheme/DatabaseModel";

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

function useForm(id) {
    const [dbm, setDbm] = useState(new DatabaseModel());

    const handleInputChange = (event) => {
        event.persist();
        let copy = Object.assign({}, dbm);
        copy[event.target.name] = event.target.value;
        setDbm(copy);
    };

    const handleLoad = (id) => {
        if (!dbm._id) {
            let apiUrl = "http://188.124.37.185:5000/api/wiki?_id=" + id;
            fetch(apiUrl)
                .then(response => response.json())
                .then(response => getObjects(response))
                .then(data => setDbm(...data));
        }
    };

    const handleSubmit = (event) => {
        if (event) {
            event.preventDefault();

            dbm["tags"] = [];
            dbm["synonyms"] = [];
            dbm["relations"] = [];
            dbm["attachments"] = [];
            let globName = "188.124.37.185";
            let apiUrl = `/api/wiki?_id=${dbm["_id"]}`;
            let sendObject = Object.assign({}, dbm);
            delete sendObject["_id"];
            fetch("http://" + globName + ":5000" + apiUrl, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(sendObject) // body data type must match "Content-Type" header
            }).then((data) => {
                console.log(data)
            });

        }
    };


    return {
        dbm,
        handleInputChange,
        handleSubmit,
        handleLoad
    }


}

export default useForm;
