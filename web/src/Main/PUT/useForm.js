import {useState} from 'react';
import DatabaseModel from "../scheme/DatabaseModel";

require('dotenv').config();
let hostName = process.env.REACT_APP_HOSTNAME;

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
            let apiPath = `/api/wiki?_id=${id}`;
            fetch(hostName + apiPath)
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
            let apiPath = `/api/wiki?_id=${dbm["_id"]}`;

            let sendObject = Object.assign({}, dbm);
            delete sendObject["_id"];
            fetch(hostName + apiPath, {
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
