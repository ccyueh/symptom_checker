import React, { Component } from 'react';
import './App.css';
import SymptomPicker from './components/symptomPicker';
import Diagnosis from './components/diagnosis';
import DiagnosisPicker from './components/diagnosisPicker';
import Frequency from './components/frequency';

class App extends Component {
  constructor() {
    super()

    this.state = {
      symptoms: [],
      diagnosis: [],
      alternatives: [],
      frequency: [],
      symptom_id: '',
      show_alternatives: false,
      show_frequency: false
    }
  }

  // gets all symptoms
  getSymptoms = async() => {
    const URL = 'http://localhost:5000/api/symptoms/retrieve';

    let response = await fetch(URL, {
      'method': 'GET',
      'headers': { 'Content-Type': 'application/json' }
    })

    let data = await response.json();
    if (data.symptoms) {
      return data.symptoms;
    } else {
      alert('No symptoms found.')
    }
  }

  // gets possible diagnoses and their frequencies based on symptom
  getDiagnoses = async(e) => {
    e.preventDefault()

    let symptom_id = e.target.symptoms.value;
    let URL = 'http://localhost:5000/api/diagnoses/retrieve?symptom_id=';
    URL += symptom_id;

    let response = await fetch(URL, {
      'method': 'GET',
      'headers': { 'Content-Type': 'application/json' }
    })

    let data = await response.json();
    if (data.diagnosis) {
      let diagnosis = data.diagnosis;
      let alternatives = data.alternatives;
      let frequency = data.frequency;

      this.setState({ diagnosis, alternatives, frequency, symptom_id });
    } else if (data.error) {
      alert(`${data.error}`);
    } else {
      alert('No diagnoses found.')
    }
  }

  // adds new diagnosis to database
  saveDiagnosis = async(symptom_id, diagnosis_id) => {
    const URL = 'http://localhost:5000/api/diagnoses/save';

    let response = await fetch(URL, {
      'method': 'POST',
      'headers': { 'Content-Type': 'application/json' },
      'body': JSON.stringify({
        'symptom_id': symptom_id,
        'diagnosis_id': diagnosis_id
      })
    })

    let data = await response.json();

    if (data.success) {
      return diagnosis_id;
    } else if (data.error) {
      alert(`${data.error}`);
    } else {
      alert('Could not save diagnosis.');
    }
  }

  showFrequency = () => {
    this.setState({ 'show_frequency': true });
    this.saveDiagnosis(this.state.symptom_id, this.state.diagnosis[0]);
  }

  showAlternatives = () => {
    this.setState({ 'show_alternatives': true});
  }

  // sets diagnosis to newly chosen diagnosis and hides alternative diagnoses dropdown/allows diagnosis frequency to be displayed
  setDiagnosis = e => {
    e.preventDefault();

    let diagnosis = e.target.diagnoses.value;
    this.saveDiagnosis(this.state.symptom_id, diagnosis.split(',')[0]);
    this.setState({
      'diagnosis': diagnosis.split(','),
      'show_alternatives': false,
      'show_frequency': true
    });
  }

  // return to initial state for new user
  reset = e => {
    this.setState({
      'diagnosis': [],
      'alternatives': [],
      'frequency': [],
      'show_alternatives': false,
      'show_frequency': false
    });
  }

  async componentDidMount() {
    // get all symptoms from API for initial dropdown menu
    let symptoms = await this.getSymptoms();
    this.setState({ symptoms });
  }

  render() {
    return (
      <div className="App row">
        <div className="col-md-6 offset-md-3 text-center">
          <h1>Symptom Checker</h1>
          { this.state.diagnosis.length == 0 &&
            <SymptomPicker
              symptoms={this.state.symptoms}
              getDiagnoses={this.getDiagnoses}
            />
          }
          { this.state.diagnosis.length > 0 &&
            !this.state.show_alternatives &&
            !this.state.show_frequency &&
            <Diagnosis
              diagnosis={this.state.diagnosis}
              showFrequency={this.showFrequency}
              showAlternatives={this.showAlternatives}
            />
          }
          { this.state.show_alternatives &&
            <DiagnosisPicker
              diagnoses={this.state.alternatives}
              setDiagnosis={this.setDiagnosis}
            />
          }
          { Object.keys(this.state.frequency).length > 0 &&
            this.state.show_frequency &&
            <div>
              <Frequency
                frequency={this.state.frequency}
                diagnosis={this.state.diagnosis[1]}
              />
              <button
                className="btn btn-primary"
                onClick={() => this.reset()}
              >
                Start Over
              </button>
            </div>
          }
        </div>
      </div>
    );
  }
}

export default App;
