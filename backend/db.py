import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# MySQL connection info from .env file
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1524")
DB_NAME = os.getenv("DB_NAME", "medivision")

# Build MySQL connection string
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define base for table models
Base = declarative_base()

# Define the HealthTestResult table structure
class HealthTestResult(Base):
    __tablename__ = 'health_results'

    id = Column(Integer, primary_key=True)
    patient_id = Column(String)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    bmi = Column(Float)
    test_date = Column(Date)
    previous_test_date = Column(Date)
    test_name = Column(String)
    value = Column(Float)
    unit = Column(String)
    reference_range = Column(String)

# Initialize the table (creates if not exists)
def init_db():
    Base.metadata.create_all(engine)
    print("Database and table created successfully.")

# Insert a single result into the DB
def insert_result(data):
    try:
        record = HealthTestResult(**data)
        session.add(record)
        session.commit()
        print(f"Inserted test result for: {data['test_name']} ({data['patient_id']})")
    except Exception as e:
        session.rollback()
        print(f"Failed to insert record: {e}")

# Run directly to create table
if __name__ == '__main__':
    init_db()
