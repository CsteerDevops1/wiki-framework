import React from 'react';
import './ModelElement.css';

const deleteObject = (id) => {
    let globName = "188.124.37.185";
    let apiUrl = `/api/wiki?_id=${id}`;

    if (window.confirm("Вы уверены, что хотите удалить этот объект?")){
        fetch("http://" + globName + ":5000" + apiUrl, {method: 'DELETE'})
            .then((data) => {
                if (data.status === 200){
                    alert("Объект успешно удален!");
                    window.location.href = '/get';
                }
            });
    }
};


function ModelElement(props) {
    return (
        <div className={"modelElement"}>

            {
                props.visibleFields.includes("name") &&
                props.model.name !== undefined &&
                props.model.name !== "" &&
                <h2><a href={"/get/" + props.model._id}>{props.model.name}</a></h2>
            }
            {
                props.visibleFields.includes("description") &&
                props.model.description !== undefined &&
                props.model.description !== "" &&
                <p>Description: <b>{props.model.description}</b></p>
            }
            {
                props.visibleFields.includes("russian_description") &&
                props.model.russian_description !== undefined &&
                props.model.russian_description !== "" &&
                <p>Description in russian: <b>{props.model.russian_description}</b></p>
            }
            {
                props.visibleFields.includes("relations") &&
                props.model.relations.length > 0 &&
                <p>Relations to other items: <b>{props.model.relations}</b></p>
            }
            {
                props.visibleFields.includes("tags") &&
                props.model.tags.length > 0 &&
                <p>Tags: <b>
                    {props.model.tags.map((item, key) =>
                        <span key={item + key} className={"tag"}>{item}</span>)
                    }
                </b></p>
            }
            {
                props.visibleFields.includes("text") &&
                props.model.text !== undefined &&
                props.model.text !== "" &&
                <p>Text: <b>{props.model.text}</b></p>
            }
            {
                props.visibleFields.includes("creationDate") &&
                props.model.creation_date !== undefined &&
                props.model.creation_date !== "" &&
                <p>Creation date: <b>{props.model.creation_date}</b></p>
            }
            {(props.model.attachments.length > 0 && props.visibleFields.includes("media")) ? (
                    <div>
                        {props.model.attachments.map((item, key) => {
                            if (/image.*/.test(item.content_type)) {
                                return <img key={key} src={"data:" + item.content_type + ";base64," + item.content_data} alt={"Graphic!"}/>
                            } else if (/audio.*/.test(item.content_type)) {
                                return <audio width={"100%"} key={key} controls
                                              src={"data:" + item.content_type + ";base64," + item.content_data}/>
                            } else if (/video.*/.test(item.content_type)) {
                                return <video width={"100%"} key={key} controls>
                                    <source type={item.content_type} src={"data:" + item.content_type + ";base64," + item.content_data}/>
                                </video>
                            } else {
                                return <embed height={"700"} width={"700"} key={key} src = {"data:" + item.content_type + ";base64," + item.content_data}/>
                            }
                        })}
                    </div>
                ) :
                (<p>No files attached</p>)}

            { (props.isButtonVisible && props.model["_id"] !== undefined) ? (
                <p>
                    <i onClick={() => deleteObject(props.model["_id"])} className={"material-icons icon-btn icon-btn__color-4"}>delete</i>
                    <a href={"/put/" + props.model._id}><i className={"material-icons icon-btn icon-btn__color-1"}>edit</i></a>
                </p>) : ""
            }

        </div>
    );
}

export default ModelElement;
