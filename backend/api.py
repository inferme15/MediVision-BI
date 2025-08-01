from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from db import engine
from models import HealthTestResult

app = Flask(__name__)
CORS(app)

Session = sessionmaker(bind=engine)

@app.route('/')
def home():
	return "Welcome to MediVision BI API! Available endpoints: /api/patients, /api/results/<patient_id>"

@app.route('/api/patients', methods=['GET'])
def get_all_patients():
	session = Session()
	try:
		patients = session.query(HealthTestResult.patient_id).distinct().all()
		result = [p[0] for p in patients]
		return jsonify(result)
	except Exception as e:
		return jsonify({"error": str(e)})
	finally:
		session.close()

@app.route('/api/results/<patient_id>', methods=['GET'])
def get_results_by_patient(patient_id):
	session = Session()
	try:
		records = session.query(HealthTestResult).filter_by(patient_id=patient_id).all()
		output = []
		for r in records:
			output.append({
				"test_name": r.test_name,
				"value": r.value,
				"unit": r.unit,
				"reference_range": r.reference_range,
				"test_date": str(r.test_date)
			})
		return jsonify(output)
	except Exception as e:
		return jsonify({"error": str(e)})
	finally:
		session.close()

if __name__ == '__main__':
	app.run(debug=True, port=5000)