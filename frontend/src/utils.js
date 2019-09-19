export const getSymptoms = async() => {
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

export const getDiagnoses = async(e) => {
  e.preventDefault()

  let symptom_id = e.target.symptoms.value;
  console.log(symptom_id);
  let URL = 'http://localhost:5000/api/diagnoses/retrieve?symptom_id=';
  URL += symptom_id;

  let response = await fetch(URL, {
    'method': 'GET',
    'headers': { 'Content-Type': 'application/json' }
  })

  let data = await response.json();
  console.log(data);
  if (data.diagnosis) {
    return data;
  } else if (data.error) {
    alert(`${data.error}`);
  } else {
    alert('No diagnoses found.')
  }
}

export const saveDiagnosis = async(symptom_id, diagnosis_id) => {
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
