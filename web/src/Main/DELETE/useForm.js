import {useState} from 'react';
import DatabaseModel from "../scheme/DatabaseModel";

function useForm(callback) {
    let qstring = "?";
    let myMap = new Map();
    const handleSubmit = (event) => {
        if (event) {
            event.preventDefault();
            //forming DELETE query, if it is empty we alert
            for (let [key, value] of myMap){
                if(value === ""){
                    myMap.delete(key);
                } else {
                    qstring = qstring + key + "=" + value + "&";
                }
            }
            if(myMap.size === 0){
                alert("Enter at least one parameter, or whole database will be wiped!");
                return 0;
            }
            let globName = "188.124.37.185";
            let apiUrl = "/api/wiki";
            fetch("http://" + globName + ":5000" + apiUrl + qstring, {
                method: 'DELETE' // body data type must match "Content-Type" header
                }).then((data) => {console.log(data); });
        }
    }
     const handleInputChange = (event) => {
       event.persist();
       myMap.set(event.target.name, event.target.value)
     }
   
     return {
       handleSubmit,
       handleInputChange
     };
   }


export default useForm;