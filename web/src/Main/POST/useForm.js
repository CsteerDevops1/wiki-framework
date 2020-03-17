import React, {useEffect, useState} from 'react';
import DatabaseModel from "../scheme/DatabaseModel";

function useForm(callback) {
 const [dbm, setDbm] = useState(new DatabaseModel());
  const handleSubmit = (event) => {
    if (event) {
        event.preventDefault();
    }
  }
  const handleInputChange = (event) => {
    event.persist();
    dbm[event.target.name] = event.target.value;
    setDbm(dbm)
    console.log(dbm);
  }
  return {
    handleSubmit,
    handleInputChange,
    dbm
  };
}

export default useForm;