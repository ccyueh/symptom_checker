from app import app, db
import os
from flask import request, jsonify
from app.models import Symptom, Diagnosis, symptom_diagnosis
from collections import Counter

@app.route('/')
def index():
    return ''

@app.route('/api/diagnoses/retrieve', methods=['GET'])
def getDiagnosis():
    symptom_id = request.args.get('symptom_id')

    if symptom_id:
        result = Symptom.query.filter_by(symptom_id=symptom_id).first()
        if result:
            diagnoses = [(d.diagnosis_id,d.diagnosis_name) for d in result.diagnoses]
            diagnosis_counts = Counter(diagnoses)
            top_diagnoses = sorted(diagnosis_counts, key=lambda x:x[1])
            
            if len(top_diagnoses) > 0:
                diagnosis = top_diagnoses[0]
                if len(top_diagnoses) > 1:
                    alternatives = top_diagnoses[1:]
                else:
                    alternatives = []

                frequency = {}
                for k, v in diagnosis_counts.items():
                    frequency[k] = v/len(diagnoses)

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
        
        symptom.diagnoses.append(diagnosis)

        db.session.add(symptom)
        db.session.commit()
    
        return jsonify({ 'success': 'Diagnosis saved.' })
    else:
        return jsonify({ 'error': 'Symptom and diagnosis IDs are required.' })

