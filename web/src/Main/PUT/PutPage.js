import React from 'react';
import '../Main.css';
import './PutPage.css';
import useForm from './useForm';
import {useParams} from "react-router-dom";

function PutPage() {
    let {id} = useParams();
    let {dbm, handleInputChange, handleLoad, handleSubmit} = useForm(id);
    handleLoad(id);

    return (
        <main>
            <h1>Edit object in a DB with ID: {id}</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor={"name"}>Название: {dbm.name} <br/>
                    <input onChange={handleInputChange} value={dbm.name} name={"name"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"russian_name"}>Название на русском: <br/>
                    <input value={ (dbm) ? dbm.russian_name : ""} onInput={handleInputChange} name={"russian_name"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"description"}>Описание: <br/>
                    <input value={ (dbm) ? dbm.description : ""} onInput={handleInputChange} name={"description"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"russian_description"}>Описание на русском: <br/>
                    <input value={ (dbm) ? dbm.russian_description : ""} onInput={handleInputChange} name={"russian_description"} type={"text"}
                           className={"form-input"}/>
                </label>

                <label htmlFor={"text"}>Текст: <br/>
                    <input onInput={handleInputChange} value={ (dbm) ? dbm.text : ""} name={"text"} type={"text"} className={"form-input"}/>
                </label>

                <input value={"Отправить"} type={"submit"}/>
            </form>
        </main>
    );
}

export default PutPage;
