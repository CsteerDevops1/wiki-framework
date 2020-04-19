import React from 'react';
import '../Main.css';
import './PostPage.css';
import useForm from './useForm';

function PostPage() {
    const {handleSubmit, handleFileSelect, preview} = useForm();
    return (
        <main>
            <h1>Upload your object to database</h1>
            <form onSubmit={handleSubmit}>

                <label>Name: <br/>
                    <input name={"name"} type={"text"} className={"form-input"}/>
                </label>

                <label>Name in russian: <br/>
                    <input name={"russian_name"} type={"text"} className={"form-input"}/>
                </label>

                <label>Description: <br/>
                    <input name={"description"} type={"text"} className={"form-input"}/>
                </label>

                <label>Description in russian: <br/>
                    <input name={"russian_description"} type={"text"} className={"form-input"}/>
                </label>

                <label>Text: <br/>
                    <input name={"text"} type={"text"} className={"form-input"}/>
                </label>

                <label>File: <br/>
                    <input name={"file"} onChange={handleFileSelect} type="file" className={"form-input"}/>
                </label>

                {preview.map(im => (
                     <img src={ im } width="300" height="300"/>
                ))}

                <input value={"Send"} type={"submit"} />
            </form>
        </main>
    );
}

export default PostPage;
