import React, {useEffect, useState} from 'react';
import '../Main.css';


function GetPage() {
    const [models, setModels] = useState(null);
    useEffect(() => {
        let globName = window.location.hostname;
        let apiUrl = "/api/wiki";

        fetch(globName+":8080"+apiUrl)
            .then(response => response.json())
            .then(data => setModels(data))
            .catch((error) => {

              });
    });


    return (
        <main>
            <h1>Get all objects</h1>
            <ul>
                {(models != null) ? models.map((item, key) =>
                    <li>
                        Название: <b>{item.name}</b><br/>
                        Описание: <b>{item.description}</b><br/>
                        <hr/>
                    </li>
                ): ""}
            </ul>
        </main>
    );
}

export default GetPage;
