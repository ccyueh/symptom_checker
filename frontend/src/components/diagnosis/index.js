import React from 'react';
import './index.css';

function Diagnosis(props) {
  return (
    <div>
      <h2 className="blue">Diagnosis:</h2>
      <h3>{props.diagnosis[1]}</h3>
      <h4>Is this diagnosis correct?</h4>
      <button
        className="btn btn-primary"
        onClick={props.showFrequency}
      >
        Yes
      </button>
      <button
        className="btn btn-primary"
        onClick={props.showAlternatives}
      >
        No
      </button>
    </div>
  );
}

export default Diagnosis;
