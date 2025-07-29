import pandas as pd
from datetime import datetime
from db import insert_result, init_db
import os

# Initialize the database and create tables if not already present
init_db()

# Step 1: Ask user to enter patient details manually
def get_patient_details():
    print("🔍 Please enter patient details:")
    patient = {}
    patient['patient_id'] = input("Patient ID: ").strip()
    patient['name'] = input("Name: ").strip()
    patient['gender'] = input("Gender (M/F): ").strip().upper()
    patient['age'] = int(input("Age: ").strip())
    patient['height_cm'] = float(input("Height (in cm): ").strip())
    patient['weight_kg'] = float(input("Weight (in kg): ").strip())
    test_date_str = input("Test Date (YYYY-MM-DD): ").strip()
    previous_date_str = input("Previous Test Date (YYYY-MM-DD or leave blank): ").strip()

    # Convert to date objects
    patient['test_date'] = datetime.strptime(test_date_str, "%Y-%m-%d").date()
    patient['previous_test_date'] = (
        datetime.strptime(previous_date_str, "%Y-%m-%d").date() if previous_date_str else None
    )

    # Calculate BMI
    height_m = patient['height_cm'] / 100
    patient['bmi'] = round(patient['weight_kg'] / (height_m ** 2), 2)

    return patient

# Step 2: Read test results from CSV and insert each row into DB
def process_csv_and_insert(csv_path, patient_info):
    try:
        df = pd.read_csv(csv_path)

        required_columns = {'Test Name', 'Value', 'Unit', 'Reference Range'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")

        for _, row in df.iterrows():
            record = {
                'patient_id': patient_info['patient_id'],
                'name': patient_info['name'],
                'gender': patient_info['gender'],
                'age': patient_info['age'],
                'height_cm': patient_info['height_cm'],
                'weight_kg': patient_info['weight_kg'],
                'bmi': patient_info['bmi'],
                'test_date': patient_info['test_date'],
                'previous_test_date': patient_info['previous_test_date'],
                'test_name': row['Test Name'],
                'value': float(row['Value']),
                'unit': row['Unit'],
                'reference_range': row['Reference Range']
            }

            insert_result(record)

        print(f"✅ Successfully inserted {len(df)} records into the database.")

    except Exception as e:
        print(f"❌ Error processing CSV: {e}")

# Step 3: Run script
if __name__ == '__main__':
    # CSV file path from Member 1
    csv_file = os.path.join("data", "processed", "sample_output.csv")

    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found at: {csv_file}")
    else:
        patient_info = get_patient_details()
        process_csv_and_insert(csv_file, patient_info)
