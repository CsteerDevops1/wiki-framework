import React, {useEffect, useState} from 'react';
import '../Main.css';


function formatAttachments(data){
    // doesn't work? to long content_data
    data.map((item) => {
        if (! typeof item.attachments === 'undefined'){
            item.attachments.map((content) => {
                content.content_data = "data:${content.content_type};base64," + content.content_data;
        })}
    })
    return data;
}

function GetPage() {
    const [models, setModels] = useState(null);
    useEffect(() => {
        let globName = window.location.hostname;
        let apiUrl = "/api/wiki";

        fetch("http://" + globName + ":5000" + apiUrl, {mode: 'no-cors'})
            .then(response => response.json())
            .then(data => formatAttachments(data))
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
                        {
                            (typeof item.attachments === 'undefined') ? "" :
                                item.attachments.map((content, key) =>
                                    <object data={content.content_data}></object>
                                
                        )}
                        <hr/>
                    </li>
                ): ""}
            </ul>
        </main>
    );
}

export default GetPage;
