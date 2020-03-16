import React from 'react';
import './ModelElement.css';

function ModelElement(props) {
    return (
        <div className={"modelElement"}>

            Название: <b>{props.model.name}</b><br/>
            Описание: <b>{props.model.description}</b><br/>
            Описание на русском: <b>{props.model.russian_description}</b><br/>
            {/*Связи: <b>{props.model.relations}</b><br/>*/}
            Тэги: <b>{props.model.tags.map((item, key) => <span key={item+key} className={"tag"}>{item}</span>)}</b><br/>
            Текст: <b>{props.model.text}</b><br/>
            Дата создания: <b>{props.model.creation_date}</b><br/>
            {/*Прикрепления: <b>{props.model.attachments}</b><br/>*/}
        </div>
    );
}

export default ModelElement;