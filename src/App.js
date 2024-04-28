import React, { useState } from 'react';
import InputScreen from './InputScreen';
import OutputScreen from './OutputScreen';
import './App.css';
import './index.css';

function App() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmissionSuccess = () => {
    setSubmitted(true);
  };

  return (
    <div className="App">
      {!submitted ? <InputScreen onSubmitSuccess={handleSubmissionSuccess} /> : <OutputScreen />}
    </div>
  );
}

export default App;
