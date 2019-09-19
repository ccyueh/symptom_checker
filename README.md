## Symptom Checker

### Installation

This project uses Flask and React.

1. `pip install flask flask-cors flask-sqlalchemy flask-migrate pytest`
2. `npm install -g create-react-app`

### Development

In the `backend/` directory:
1. `export FLASK_APP=main.py`
2. `export FLASK_DEBUG=1`
3. `flask run`

The backend API should be running at [http://localhost:5000/](http://localhost:5000/).

In the `frontend/` directory:
1. `npm start`

Open [http://localhost:3000](http://localhost:3000) to view the project.

### API Documentation

The API provides information about possible diagnoses for several symptoms, as well as how frequently each diagnosis is associated with each symptom.

#### Endpoints

##### GET api/symptoms/retrieve

Returns all symptoms in the database.

**Parameters:** None

**Sample request:**
`curl "http://localhost:5000/api/symptoms/retrieve"`

**Sample response:**
```
{
  "symptoms": [
    [
      1, 
      "Sore Throat"
    ], 
    [
      2, 
      "Itchy Rash"
    ], 
    [
      3, 
      "Runny Nose"
    ]
  ]
}
```
Each symptom is returned in [symptom_id, symptom_name] format.

##### GET api/diagnoses/retrieve

Returns most likely diagnosis, alternative diagnoses, and diagnosis frequencies for a given symptom. 

**Parameters (Required):**
*symptom_id (Integer)*
The ID of the symptom.

**Sample request:**
`curl "http://localhost:5000/api/diagnoses/retrieve?symptom_id=1"`

**Sample response:**
```
{
  "alternatives": [
    [
      1, 
      "Acid Reflux Disease"
    ], 
    [
      6, 
      "Bronchitis"
    ], 
    [
      21, 
      "Seasonal Allergies"
    ], 
    [
      24, 
      "Strep Throat"
    ], 
    [
      27, 
      "Viral Throat Infection"
    ], 
    [
      2, 
      "Acute Bacterial Sinusitis"
    ], 
    [
      15, 
      "Middle Ear Infection"
    ], 
    [
      16, 
      "Mononucleosis Infection"
    ]
  ], 
  "diagnosis": [
    11, 
    "Common Cold"
  ], 
  "frequency": {
    "Acid Reflux Disease": 0.2, 
    "Acute Bacterial Sinusitis": 0.04, 
    "Bronchitis": 0.12, 
    "Common Cold": 0.32, 
    "Middle Ear Infection": 0.04, 
    "Mononucleosis Infection": 0.04, 
    "Seasonal Allergies": 0.08, 
    "Strep Throat": 0.08, 
    "Viral Throat Infection": 0.08
  }
}
```
Diagnosis and alternatives are given in [diagnosis_id,diagnosis_name] format, with alternatives being a list. Frequency is given as a dictionary with diagnosis names as the keys and diagnosis frequency as the values.

##### POST api/diagnoses/save
Adds a new record of a diagnosis for a symptom.

**Parameters (Required):**
*symptom_id (Integer)*
The ID of the symptom.

*diagnosis_id (Integer)*
The ID of the diagnosis.

**Sample request:**
`curl -i -X POST -H "Content-Type:application/json" http://localhost:5000/api/diagnoses/save -d '{"symptom_id":1,"diagnosis_id":11}'`

**Sample response:**
```
{
  "success": "Diagnosis saved."
}
```

#### Testing

Run `pytest` to run the API tests. 

Each endpoint is tested to make sure it is valid. 

For symptoms, it cannot be an empty list (since users must be able to choose a symptom) and both symptom ID and name must be given.

For diagnoses, both valid and invalid symptom IDs were tested for formatting and expected values.

For saving diagnoses, both valid and invalid symptom/diagnosis IDs were tested.
