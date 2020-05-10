import React, {useEffect, useState} from 'react';
import '../Main.css';
import DatabaseModel from "../scheme/DatabaseModel";
import ModelElement from "../items/ModelElement";
 
 
export function getObjects(response) {
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
 
function GetPage() {
    const [models, setModels] = useState(null);
    useEffect(() => {
        if (!models) {
            // let globName = window.location.hostname;
            let globName = "wf.csteer.pro";
            let apiUrl = "/api/wiki";
            fetch("https://" + globName + apiUrl)
                .then(response => response.json())
                .then(response => getObjects(response))
                .then(data => setModels(data));
        }
    }, [models]);
 
 
    return (
        <main>
            <h1>All objects</h1>
            <a href={"/post"} className={"link-btn"}>Create new</a>
            <ul>
                {(models != null) ? models.map((item, key) => <li key={item._id}>
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
                ) : "Nothing found!"}
            </ul>
 
 
        </main>
    );
}
 
export default GetPage;
