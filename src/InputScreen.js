import React, { useState } from 'react';
import axios from 'axios';

function InputScreen({ onSubmitSuccess }) {
  const [question, setQuestion] = useState('');
  const [documents, setDocuments] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const docArray = documents.split('\n').filter(doc => doc.length);
    const payload = {
      question,
      documents: docArray,
    };

    try {
      await axios.post('http://localhost:8000/submit_question_and_documents', payload);
      setStatus('Submitted! Processing...');
      onSubmitSuccess();  // Callback to notify App of successful submission
    } catch (error) {
      setStatus('Error submitting data');
      console.error('There was an error!', error);
    }
  };

  return (
    <div className="form-container">
      <h1 className="header">Extract The Facts</h1>
      <p className="subheader">From Any Document Related To A Question</p>
      <h1>Submit Your Question</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Question:
          <input type="text" value={question} onChange={(e) => setQuestion(e.target.value)} />
        </label>
        <label>
          Document URLs (one per line):
          <textarea value={documents} onChange={(e) => setDocuments(e.target.value)} />
        </label>
        <button type="submit">Submit</button>
      </form>
      <p>{status}</p>
    </div>
  );
}

export default InputScreen;