from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base
Base = declarative_base()
class HealthTestResult(Base):
	__tablename__ = 'health_results'
	id = Column(Integer, primary_key=True, autoincrement=True)
	patient_id = Column(String, nullable=False)
	name = Column(String)
	gender = Column(String)
	age = Column(Integer)
	height_cm = Column(Float)
	weight_kg = Column(Float)
	bmi = Column(Float)
	test_date = Column(Date)
	previous_test_date = Column(Date)
	test_name = Column(String, nullable=False)
	value = Column(Float)
	unit = Column(String)
	reference_range = Column(String)
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base
Base = declarative_base()
class HealthTestResult(Base):
	__tablename__ = 'health_results'
	id = Column(Integer, primary_key=True, autoincrement=True)
	patient_id = Column(String, nullable=False)
	name = Column(String)
	gender = Column(String)
	age = Column(Integer)
	height_cm = Column(Float)
	weight_kg = Column(Float)
	bmi = Column(Float)
	test_date = Column(Date)
	previous_test_date = Column(Date)
	test_name = Column(String, nullable=False)
	value = Column(Float)
	unit = Column(String)
	reference_range = Column(String)
