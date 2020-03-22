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

                <label htmlFor={"name"}>Name: <br/>
                    <input onInput={handleInputChange} name={"name"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"russian_name"}>Name in russian: <br/>
                    <input onInput={handleInputChange} name={"russian_name"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"description"}>Description: <br/>
                    <input onInput={handleInputChange} name={"description"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"russian_description"}>Description in russian: <br/>
                    <input onInput={handleInputChange} name={"russian_description"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"text"}>Text: <br/>
                    <input onInput={handleInputChange} name={"text"} type={"text"} className={"form-input"}/>
                </label>

                <label >File: <br/>
                    <input onChange={fileSelectedHandler} type="file" className={"form-input"}/>
                </label>

                <input value={"Send"} type={"submit"} />
            </form>
        </main>
    );
}

export default PostPage;
