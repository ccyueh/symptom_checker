from app import app, db
import os
from flask import request, jsonify
from app.models import Symptom, Diagnosis, Record
from collections import Counter

@app.route('/')
def index():
    return ''

@app.route('/api/diagnoses/retrieve', methods=['GET'])
def getDiagnosis():
    symptom_id = request.args.get('symptom_id')

    if symptom_id:
        symptom = Symptom.query.filter_by(symptom_id=symptom_id).first()
        if symptom:
            records = db.session.query(Record.record_id, Record.symptom_id, Diagnosis.diagnosis_id, Diagnosis.diagnosis_name).join(Record).filter_by(symptom_id=symptom_id).all()
            diagnoses = [(d.diagnosis_id,d.diagnosis_name) for d in records]
            diagnosis_counts = Counter(diagnoses)
            top_diagnoses = diagnosis_counts.most_common()
            if len(top_diagnoses) > 0:
                diagnosis = top_diagnoses[0]
                if len(top_diagnoses) > 1:
                    alternatives = top_diagnoses[1:]
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

@app.route('/api/diagnoses/save', methods=['POST'])
def saveDiagnosis():
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

