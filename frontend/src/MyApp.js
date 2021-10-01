import React, {useState, useEffect} from 'react';
import axios from 'axios';
import Table from './Table';
import Form from './Form';


function MyApp() {
  const [characters, setCharacters] = useState([]);

  useEffect(() => {
    fetchAll().then( result => {
       if (result)
          setCharacters(result);
     });
  }, [] );

  function removeOneCharacter (index) {
    const updated = characters.filter((character, i) => {
        return i !== index
      });
      setCharacters(updated);
  }

  async function fetchAll(){
    try {
       const response = await axios.get('http://localhost:5000/users');
       return response.data.users_list;
    }
    catch (error){
       //We're not handling errors. Just logging into the console.
       console.log(error); 
       return false;         
    }
 }

 function updateList(person) { 
  makePostCall(person).then( result => {
  if (result)
     setCharacters([...characters, person] );
  });
}

 async function makePostCall(person){
    try {
     const response = await axios.post('http://localhost:5000/users', person);
     console.log(response.data)
     return response.data; 
    }
    catch (error) {
     console.log(error);
     return false;
    }
  }

  return (
    <div className="container">
      <Table characterData={characters} removeCharacter={removeOneCharacter} />
      <Form handleSubmit={updateList} />
    </div>
  );  
}


export default MyApp;