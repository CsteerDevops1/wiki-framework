import React from 'react';
import './ModelElement.css';

function ModelElement(props) {
    return (
        <div className={"modelElement"}>

            {props.model.name !== undefined && props.model.name !== "" &&
            <p>Name: <b>{props.model.name}</b></p>
            }
            {props.model.description !== undefined && props.model.description !== "" &&
            <p>Description: <b>{props.model.description}</b></p>
            }
            {props.model.russian_description !== undefined && props.model.russian_description !== "" &&
            <p>Description in russian: <b>{props.model.russian_description}</b></p>
            }
            {props.model.relations.length > 0 &&
            <p>Relations to other items: <b>{props.model.relations}</b></p>
            }
            {props.model.relations.length > 0 &&
            <p>Tags: <b>
                {props.model.tags.map((item, key) =>
                    <span key={item + key} className={"tag"}>{item}</span>)
                }
            </b></p>
            }
            {props.model.text !== undefined && props.model.text !== "" &&
            <p>Text: <b>{props.model.text}</b></p>
            }
            {props.model.creation_date !== undefined && props.model.creation_date !== "" &&
            <p>Creation date: <b>{props.model.creation_date}</b></p>
            }
            {(props.model.attachments.length > 0) ? (
                    <div>
                        {props.model.attachments.map((item, key) => {
                            if (item.content_type === "image/jpg" || item.content_type === "image/jpeg" || item.content_type === "image/png") {
                                return <img key={key} src={"data:image/png;base64," + item.content_data} alt={"Graphic!"}/>
                            } else if (item.content_type === "audio/mp4") {
                                return <audio width={"100%"} key={key} controls src={"data:audio/mp4;base64," + item.content_data} />
                            } else if (item.content_type === "video/mp4") {
                                return <video width={"100%"} key={key} controls>
                                	<source type={"video/mp4"} src={"data:video/mp4;base64," + item.content_data} />
                                </video>
                            } else {
                                return <br key={key}/>
                            }
                        })}
                    </div>
                ) :
                (<p>No files attached</p>)}

                <p>
                    <i className={"material-icons icon-btn icon-btn__color-4"}>delete</i>
                    <a href={"/put/" + props.model._id}><i className={"material-icons icon-btn icon-btn__color-1"}>edit</i></a>
                </p>

        </div>
    );
}

export default ModelElement;