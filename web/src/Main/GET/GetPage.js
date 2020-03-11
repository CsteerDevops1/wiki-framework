import React, {useEffect, useState} from 'react';
import '../Main.css';

function GetPage() {
    const [models, setModels] = useState(null);
    useEffect(() => {
        fetch('http://localhost:8080/api/wiki')
            .then(response => response.json())
            .then(data => setModels(data));
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
