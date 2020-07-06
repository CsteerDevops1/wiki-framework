import React from 'react';
import '../Main.css';
import ModelElement from "../items/ModelElement";
import useForm from "./useForm"

 
function SearchPage() {
    const {handleSubmit, models} = useForm();

    return (
        <main>
            <h1>Write some filters here</h1>
            <form onSubmit={handleSubmit}>

                <label>Name: <br/>
                    <input name={"name"} type={"text"} className={"form-input"}/>
                </label>
                    
                <input value={"Send"} type={"submit"} />
            </form>

            <ul>
                {((models != null) && (models.length === 0))  ? <div>Nothing found!</div> :
                (models != null) ? models.map((item, key) => 
                <li key={item._id}>
                        <ModelElement
                            visibleFields={[
                                "name",
                                "russian_description",
                                "description",
                                "media"
                            ]}
 
                            isButtonVisible={false}
                            model={item}/>
                    </li>
                ) :  ""}
            </ul>
                  
 
        </main>
    );
}
 
export default SearchPage;
