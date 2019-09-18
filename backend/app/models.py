from app import app, db

symptom_diagnosis = db.Table('symptom_diagnosis', db.Model.metadata,
    db.Column('symptom_id', db.Integer, db.ForeignKey('symptom.symptom_id')), 
    db.Column('diagnosis_id', db.Integer, db.ForeignKey('diagnosis.diagnosis_id'))
)

class Symptom(db.Model):
    symptom_id = db.Column(db.Integer, primary_key=True)
    symptom_name = db.Column(db.String(100))
    
    diagnoses = db.relationship('Diagnosis', secondary=symptom_diagnosis, backref='symptoms')

class Diagnosis(db.Model):
    diagnosis_id = db.Column(db.Integer, primary_key=True)
    diagnosis_name = db.Column(db.String(100))
