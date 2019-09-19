import React from 'react';
import './index.css';

function Frequency(props) {
  return (
    <div>
      <p>Thank you for confirming your diagnosis. Here is likelihood of each diagnosis for your symptom:</p>
      <table className="table">
        <thead>
          <tr>
            <th>Diagnosis</th>
            <th>Frequency</th>
          </tr>
        </thead>
        <tbody>
          {Object.keys(props.frequency).map((freq, index) =>
            <tr
              key={index}
              className={freq == props.diagnosis ? "bg-gray" : "" }
            >
              <td>{freq}</td>
              <td>{(props.frequency[freq] * 100).toFixed(0)}%</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Frequency;
