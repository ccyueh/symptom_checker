import React from 'react';
import './index.css';

function SymptomPicker(props) {
  return (
    <form onSubmit={props.getDiagnoses}>
      <div>
        <p>Which symptom are you currently experiencing?</p>
        <select name="symptoms">
          {props.symptoms.map(symptom =>
            <option key={symptom[0]} value={symptom[0]}>
              {symptom[1]}
            </option>
          )}
        </select>
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </div>
    </form>
  );
}

export default SymptomPicker;
