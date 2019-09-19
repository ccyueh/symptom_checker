import pytest
import requests
import json

url = 'http://127.0.0.1:5000/'

def test_index_page():
    r = requests.get(url) 
    assert r.status_code == 200

def test_get_symptoms():
    r = requests.get(url + 'api/symptoms/retrieve')
    data = r.json()
    symptoms = list(data['symptoms'])

    assert r.status_code == 200
    assert len(symptoms) > 0
    assert set([len(s) for s in symptoms]) == {2} # each "symptom" should be formatted as [id, name]

def test_get_diagnoses():
    r = requests.get(url + 'api/diagnoses/retrieve')
    assert r.status_code == 200

def test_has_diagnoses():
    r = requests.get(url + 'api/diagnoses/retrieve?symptom_id=1')
    data = r.json()
    diagnosis = data['diagnosis']
    alternatives = data['alternatives']
    frequency = data['frequency']

    assert r.status_code == 200
    assert len(diagnosis) == 2 # [diagnosis_id, diagnosis_name]
    assert set([len(d) for d in alternatives]) == {2}    
    assert "Bronchitis" in frequency
    assert min(frequency.values()) > 0 # frequency must be greater than 0 

def test_has_no_diagnoses():
    r = requests.get(url + 'api/diagnoses/retrieve?symptom_id=100')
    data = r.json()
    error = data['error']

    assert r.status_code == 200
    assert error == 'Symptom not found.'

def test_save_diagnosis():
    r = requests.post(url + 'api/diagnoses/save')
    assert r.status_code == 200

def test_success_diagnosis():
    r = requests.post(
        url + 'api/diagnoses/save', 
        json = {'symptom_id': 1, 'diagnosis_id': 1}
    )
    data = r.json()
    success = data['success']

    assert r.status_code == 200
    assert success == 'Diagnosis saved.'

def test_fail_diagnosis():
    r = requests.post(
        url + 'api/diagnoses/save', 
        json = {'symptom_id': 10, 'diagnosis_id': 100}
    )
    data = r.json()
    error = data['error']

    assert r.status_code == 200
    assert error == 'Symptom and/or diagnosis not found.'
