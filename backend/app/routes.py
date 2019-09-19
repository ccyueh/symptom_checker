from app import app, db
import os
from flask import request, jsonify
from app.models import Symptom, Diagnosis, Record
from collections import Counter

@app.route('/')
def index():
    return ''

@app.route('/api/symptoms/retrieve', methods=['GET'])
def getSymptoms():
    try:
        results = db.session.query(Symptom).all()
        symptoms = [(s.symptom_id, s.symptom_name.title()) for s in results]

        return jsonify({ 'symptoms': symptoms })
    except:
        return jsonify({ 'error': 'No symptoms found.' })

@app.route('/api/diagnoses/retrieve', methods=['GET'])
def getDiagnosis():
    try:
        symptom_id = request.args.get('symptom_id')

        if symptom_id:
            symptom = Symptom.query.filter_by(symptom_id=symptom_id).first()
            if symptom:
                # select all cases of diagnoses in the record that match the given symptom
                records = db.session.query(
                    Record.record_id, 
                    Record.symptom_id, 
                    Diagnosis.diagnosis_id, 
                    Diagnosis.diagnosis_name
                ).join(Record).filter_by(symptom_id=symptom_id).all()

                diagnoses = [(d.diagnosis_id,d.diagnosis_name.title()) for d in records]
                diagnosis_counts = Counter(diagnoses) # gets diagnosis counts
                top_diagnoses = diagnosis_counts.most_common() # sorts diagnosis counts
                if len(top_diagnoses) > 0:
                    diagnosis = top_diagnoses[0][0] # first diagnosis in list will have greatest frequency (or be tied for greatest frequency)
                    if len(top_diagnoses) > 1:
                        alternatives = [d[0] for d in top_diagnoses[1:]] # remaining diagnoses
                    else:
                        alternatives = []

                    frequency = {}
                    for k, v in diagnosis_counts.items():
                        frequency[k[1]] = v/len(diagnoses)

                    return jsonify({
                        'diagnosis': diagnosis,
                        'alternatives': alternatives,
                        'frequency': frequency
                    })
                else:
                    return jsonify({ 'error': 'No diagnosis found.' })
            else:
                return jsonify({ 'error': 'Symptom not found.' })
        else:
            return jsonify({ 'error': 'Symptom ID required.' })
    except:
        return jsonify({ 'error': 'No diagnoses found.' })

@app.route('/api/diagnoses/save', methods=['POST'])
def saveDiagnosis():
    try:
        data = request.json

        symptom_id = data.get('symptom_id')
        diagnosis_id = data.get('diagnosis_id')

        if symptom_id and diagnosis_id:
            symptom = db.session.query(Symptom).filter_by(symptom_id=symptom_id).first()
            diagnosis = db.session.query(Diagnosis).filter_by(diagnosis_id=diagnosis_id).first()

            if symptom and diagnosis:
                record = Record(symptom_id=symptom_id, diagnosis_id=diagnosis_id)

                db.session.add(record)
                db.session.commit()

                return jsonify({ 'success': 'Diagnosis saved.' })
            else:
                return jsonify({ 'error': 'Symptom and/or diagnosis not found.' })
        else:
            return jsonify({ 'error': 'Symptom and diagnosis IDs are required.' })
    except:
        return jsonify({ 'error': 'Could not save diagnosis.' })
