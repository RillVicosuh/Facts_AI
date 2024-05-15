import React, { useState, useEffect } from 'react';
import axios from 'axios';

function OutputScreen() {
  const [facts, setFacts] = useState([]);
  const [status, setStatus] = useState('Loading...');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data } = await axios.get('http://factai-alb1-1373833785.us-east-2.elb.amazonaws.com/api/get_question_and_facts');
        if (data.status === 'done') {
          setFacts(data.facts);
          setStatus('');
        } else {
          setStatus('Processing...');
        }
      } catch (error) {
        setStatus('Failed to fetch facts');
        console.error('Error fetching facts:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="output-container">
      <h1>Extracted Facts</h1>
      {status ? <p>{status}</p> : (
        <div className="facts-container">
          <ul>{facts.map((fact, index) => <li key={index}>{fact}</li>)}</ul>
        </div>
      )}
    </div>
  );
}

export default OutputScreen;