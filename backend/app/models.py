from app import app, db

class Symptom(db.Model):
    symptom_id = db.Column(db.Integer, primary_key=True)
    symptom_name = db.Column(db.String(100))

class Diagnosis(db.Model):
    diagnosis_id = db.Column(db.Integer, primary_key=True)
    diagnosis_name = db.Column(db.String(100))

class Record(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    symptom_id = db.Column('symptom_id', db.Integer, db.ForeignKey('symptom.symptom_id'))
    diagnosis_id = db.Column('diagnosis_id', db.Integer, db.ForeignKey('diagnosis.diagnosis_id')) 
