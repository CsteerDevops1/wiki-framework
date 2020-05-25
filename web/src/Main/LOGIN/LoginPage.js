import React from 'react';
import '../Main.css';

require('dotenv').config();
let hostName = process.env.REACT_APP_HOSTNAME;
let apiPath = "/api/wiki/auth/login";
sessionStorage.setItem('token', localStorage.getItem('token')); 


const handleSubmit = (event) => {
    if(event) {
        const encodedValue = encodeURIComponent(window.event.target.mail.value);
        event.preventDefault();
        fetch(hostName + apiPath + `?mail=${encodedValue}`, {
                method: 'GET',
                }).then((data) => {
                data.text().then((text) => {
                    localStorage.setItem('token', JSON.parse(text).access_token)})
                })
    }
}


function LoginPage() {
    return (
        <main>
            <h1>Login page</h1>

            <form onSubmit={handleSubmit}>
                <label>Insert any email here: <br/>
                    <input name={"mail"} type={"text"} className={"form-input"}/>
                </label>
                <input value={"Send"} type={"submit"} />
            </form>

        </main>
    );
}

export default LoginPage;

