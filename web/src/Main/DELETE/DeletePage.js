import React from 'react';
import '../Main.css';
import './DeletePage.css';
import useForm from './useForm';


function DeletePage() {
    const {handleInputChange, handleSubmit, fileSelectedHandler} = useForm();

    return (
        <main>
            <h1>Enter filters to delete item(s)</h1>

            <form onSubmit={handleSubmit}>

                <label htmlFor={"name"}>Name: <br/>
                    <input onInput={handleInputChange} name={"name"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"russian_name"}>Name in russian: <br/>
                    <input onInput={handleInputChange} name={"russian_name"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"_id"}>ID: <br/>
                    <input onInput={handleInputChange} name={"_id"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"description"}>Description: <br/>
                    <input onInput={handleInputChange} name={"description"} type={"text"} className={"form-input"}/>
                </label>

                <label htmlFor={"regex"}>Regex string: <br/>
                    <input onInput={handleInputChange} name={"regex"} type={"text"} className={"form-input"}/>
                </label>

                <input value={"Send"} type={"submit"} />
            </form>
        </main>
    );
}

export default DeletePage;
