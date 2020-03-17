import React from 'react';
import './ModelElement.css';

function ModelElement(props) {
    return (
        <div className={"modelElement"}>

            {props.model.name !== undefined && props.model.name !== "" &&
            <p>Название: <b>{props.model.name}</b></p>
            }
            {props.model.description !== undefined && props.model.description !== "" &&
            <p>Описание: <b>{props.model.description}</b></p>
            }
            {props.model.russian_description !== undefined && props.model.russian_description !== "" &&
            <p>Описание на русском: <b>{props.model.russian_description}</b></p>
            }
            {props.model.relations.length > 0 &&
            <p>Связи: <b>{props.model.relations}</b></p>
            }
            {props.model.relations.length > 0 &&
            <p>Тэги: <b>
                {props.model.tags.map((item, key) =>
                    <span key={item + key} className={"tag"}>{item}</span>)
                }
            </b></p>
            }
            {props.model.text !== undefined && props.model.text !== "" &&
            <p>Текст: <b>{props.model.text}</b></p>
            }
            {props.model.creation_date !== undefined && props.model.creation_date !== "" &&
            <p>Дата создания: <b>{props.model.creation_date}</b></p>
            }
            {(props.model.attachments.length > 0) ? (
                    <div>
                        {props.model.attachments.map((item, key) => {
                            if (item.content_type === "image/jpg") {
                                return <img key={key} src={"data:image/png;base64," + item.content_data}/>
                            } else if (item.content_type === "audio/mp4") {
                                return <audio key={key} controls src={"data:audio/mp4;base64," + item.content_data} />
                            } else if (item.content_type === "video/mp4") {
                                return <video key={key} controls>
                                	<source type={"video/mp4"} src={"data:video/mp4;base64," + item.content_data} />
                                </video>
                            } else {
                                return <br key={key}/>
                            }
                        })}
                    </div>
                ) :
                (<p>Нет прикрепленных файлов</p>)}

        </div>
    );
}

export default ModelElement;