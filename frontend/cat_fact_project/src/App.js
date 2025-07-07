import './App.css';
import api from './api'
import axios from 'axios';

import React, { useState, useEffect } from 'react';


const App = () => {
  const [items, setItems] = useState([]); //Holds database items
  const [inputFact, setInputFact] = useState(''); //Holds new inputted cat fact

  const handleSubmit = async (event) =>{
    event.preventDefault();
    alert("New Cat Fact Added: " + inputFact); //Alert for when a new cat fact is added

    try { //Get new inputted cat fact
      const response = await axios.post('http://127.0.0.1:8000/catfacts', {
        fact: inputFact
      });
      console.log(response.data);
      setItems([...items, { id: Date.now(), fact: inputFact, created_at: new Date().toISOString()}]); //New cat fact
      setInputFact('');
    } catch (error) {
      console.error("Error saving to backend:", error);
    }
  }
  

  const fetchCatFacts = async () => { //Fetch cat facts from database
    const response = await api.get('/catfacts/');
    setItems(response.data)

  };

  useEffect(() => { //Load the new cat facts
    const loadData = async () => {
      await fetchCatFacts();
    };
    loadData();
  }, []);

  return (
    <><div className="App">
      <header className="App-header">
        <p>
          Welcome to the Cat Fact Tracker!
        </p>
      </header>
    </div>
    <form onSubmit={handleSubmit} className='center-form'> 
          <input type = "text" value = {inputFact} onChange = {(e) => setInputFact(e.target.value)} placeholder='Enter New Cat Fact... meow'/>
          <input type = "submit" />
    </form>
    <div className='container'>
        <h2 className='text-center my-4 table-title'>Five Cat Facts</h2>
        <table className='table table-striped table-bordered table-color'>
          <thead className='table-dark'>
            
          </thead>
          <tbody>

            {items.map((item, index) => (
              <tr key={item.id}>
                <td className = 'number-facts'>{index + 1}.</td>
                <td className = 'facts'>{item.fact}</td>
                
              </tr>
            ))}
          </tbody>
        </table>
        
      </div></>
  
  );
}

export default App;
