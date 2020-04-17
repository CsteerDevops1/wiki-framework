import React, {useEffect, useState} from 'react';
import '../Main.css';
import {useParams} from "react-router-dom";
import useForm from "../PUT/useForm";
import DatabaseModel from "../scheme/DatabaseModel";
import ModelElement from "../items/ModelElement";


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

function GetPageById() {
    let {id} = useParams();
    const [model, setModel] = useState(null);
    useEffect(() => {
        if (!model && id !== undefined) {
            // let globName = window.location.hostname;
            let globName = "188.124.37.185";
            let apiUrl = `/api/wiki?_id=${id}`;
            fetch("http://" + globName + ":5000" + apiUrl)
                .then(response => response.json())
                .then(response => getObjects(response))
                .then(data => setModel(data[0]));
        }
    }, [model]);

    return (
        <main>
             {(model != null) ? (
            <ModelElement
                visibleFields={[
                    "name",
                    "russian_description",
                    "description",
                    "media",
                    "relations",
                    "tags",
                    "text",
                    "creationDate"
                ]}

                isButtonVisible={true}
                model={model}/>) : ""}
            <a href={"/get"} className={"link-btn"}>Return back</a>
        </main>
    );
}

export default GetPageById;
