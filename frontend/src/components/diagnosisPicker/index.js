import React from 'react';
import './index.css';

function DiagnosisPicker(props) {
  return (
    <form onSubmit={props.setDiagnosis}>
      <div>
        <p>Which diagnosis is correct?</p>
        <select name="diagnoses">
          {props.diagnoses.map(diagnosis =>
            <option key={diagnosis[0]} value={diagnosis}>
              {diagnosis[1]}
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

export default DiagnosisPicker;
