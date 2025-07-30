import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const featureNames = [
  'Gender',
  'Country',
  'Occupation',
  'self_employed',
  'family_history',
  'treatment',
  'Days_Indoors',
  'Growing_Stress',
  'Changes_Habits',
  'Mental_Health_History',
  'Mood_Swings',
  'Coping_Struggles',
  'Work_Interest',
  'Social_Weakness',
  'mental_health_interview',
  'care_options',
];

function App() {
  const initialFeatures = featureNames.reduce((acc, feature) => {
    acc[feature] = '';
    return acc;
  }, {});

  const [features, setFeatures] = useState(initialFeatures);
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e, feature) => {
    setFeatures({
      ...features,
      [feature]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Convert features to array in correct order
    const featureArray = featureNames.map((feature) => {
      const val = features[feature];
      // Try to parse numeric values, else keep as string
      const numVal = parseFloat(val);
      return isNaN(numVal) ? val : numVal;
    });

    // Basic validation: check no empty values
    if (featureArray.some((val) => val === '')) {
      setError('Please fill in all feature fields.');
      setResult('');
      return;
    }

    setError('');
    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', {
        features: featureArray,
      });
      if (response.data.error) {
        setResult('');
        setError(response.data.error);
      } else {
        setResult(response.data.prediction);
        setError('');
      }
    } catch (error) {
      console.error('Error:', error);
      setResult('');
      setError('Prediction failed.');
    }
  };

  return (
    <div className="App">
      <h1>Mental Health Predictor</h1>
      <form onSubmit={handleSubmit}>
        {featureNames.map((feature) => (
          <div key={feature} style={{ marginBottom: '10px' }}>
            <label htmlFor={feature} style={{ display: 'block', fontWeight: 'bold' }}>
              {feature}:
            </label>
            <input
              type="text"
              id={feature}
              value={features[feature]}
              onChange={(e) => handleChange(e, feature)}
              style={{ width: '300px' }}
            />
          </div>
        ))}
        {error && <div className="error">{error}</div>}
        <button type="submit">Predict</button>
      </form>
      <h2>Result: {result}</h2>

      {/* Floating objects */}
      <div className="floating-object small" style={{ top: '10%', left: '5%' }}></div>
      <div className="floating-object medium" style={{ top: '20%', right: '10%' }}></div>
      <div className="floating-object large" style={{ top: '70%', left: '15%' }}></div>
      <div className="floating-object small" style={{ top: '80%', right: '20%' }}></div>
      <div className="floating-object medium" style={{ top: '50%', left: '50%' }}></div>
    </div>
  );
}

export default App;
