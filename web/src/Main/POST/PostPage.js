import React from 'react';
import '../Main.css';
import './PostPage.css';
import useForm from './useForm';


function PostPage() {
    const {handleInputChange, handleSubmit, fileSelectedHandler} = useForm();

    return (
        <main>
            <h1>Upload your object to database</h1>
            <form onSubmit={handleSubmit}>

                <label htmlFor={"name"}>Название: <br/>
                    <input onInput={handleInputChange} name={"name"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"russian_name"}>Название на русском: <br/>
                    <input onInput={handleInputChange} name={"russian_name"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"description"}>Описание: <br/>
                    <input onInput={handleInputChange} name={"description"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"russian_description"}>Описание на русском: <br/>
                    <input onInput={handleInputChange} name={"russian_description"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"text"}>Текст: <br/>
                    <input onInput={handleInputChange} name={"text"} type={"text"} className={"form-input"}/>
                </label>

                <label >Файл: <br/>
                    <input onChange={fileSelectedHandler} type="file" className={"form-input"}/>
                </label>

                <input value={"Отправить"} type={"submit"} />
            </form>
        </main>
    );
}

export default PostPage;
