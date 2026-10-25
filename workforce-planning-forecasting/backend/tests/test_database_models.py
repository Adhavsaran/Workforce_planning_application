from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models.attrition_prediction import AttritionPrediction
from app.models.department import Department
from app.models.employee import Employee
from app.models.forecast import Forecast
from app.models.recommendation import Recommendation
from app.models.user import User
from app.models.workforce_history import WorkforceHistory
from app.schemas.employee import EmployeeCreate


@pytest.fixture
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        yield session


def test_department_can_be_created(db_session: Session) -> None:
    dept = Department(name="IT", description="Information Technology")
    db_session.add(dept)
    db_session.commit()
    assert db_session.query(Department).count() == 1


def test_employee_can_be_created_and_reference_department(db_session: Session) -> None:
    department = Department(name="Finance", description="Finance team")
    db_session.add(department)
    db_session.commit()

    employee = Employee(
        employee_id="EMP1001",
        name="Alicia Brown",
        department_id=department.id,
        job_role="Financial Analyst",
        age=29,
        gender="F",
        experience_years=5.5,
        joining_date=date(2022, 2, 15),
        salary=90000,
        performance_score=88,
        satisfaction_score=8.3,
        employment_type="FULL_TIME",
        location="Chicago",
        attrition_status="ACTIVE",
    )
    db_session.add(employee)
    db_session.commit()

    saved_employee = db_session.query(Employee).filter(Employee.employee_id == "EMP1001").first()
    assert saved_employee is not None
    assert saved_employee.department_id == department.id


def test_workforce_history_references_department(db_session: Session) -> None:
    department = Department(name="Sales", description="Sales operations")
    db_session.add(department)
    db_session.commit()

    history = WorkforceHistory(
        department_id=department.id,
        year=2025,
        month=1,
        employee_count=120,
        employees_hired=7,
        employees_left=2,
        business_growth=4.5,
        project_count=12,
    )
    db_session.add(history)
    db_session.commit()

    saved_history = db_session.query(WorkforceHistory).first()
    assert saved_history is not None
    assert saved_history.department_id == department.id


def test_forecast_references_department(db_session: Session) -> None:
    department = Department(name="Operations", description="Operations team")
    db_session.add(department)
    db_session.commit()

    forecast = Forecast(
        department_id=department.id,
        forecast_period="2027-Q4",
        forecasted_employee_count=140,
        model_name="Linear Regression",
        confidence_score=0.87,
    )
    db_session.add(forecast)
    db_session.commit()

    saved_forecast = db_session.query(Forecast).first()
    assert saved_forecast is not None
    assert saved_forecast.department_id == department.id


def test_attrition_prediction_references_employee(db_session: Session) -> None:
    department = Department(name="IT", description="Technology")
    db_session.add(department)
    db_session.commit()

    employee = Employee(
        employee_id="EMP2001",
        name="Rafael Stone",
        department_id=department.id,
        job_role="Software Engineer",
        age=33,
        gender="M",
        experience_years=7.0,
        joining_date=date(2020, 11, 3),
        salary=120000,
        performance_score=90,
        satisfaction_score=6.8,
        employment_type="FULL_TIME",
        location="Seattle",
        attrition_status="ACTIVE",
    )
    db_session.add(employee)
    db_session.commit()

    prediction = AttritionPrediction(
        employee_id=employee.id,
        prediction_date=date(2026, 10, 5),
        attrition_probability=0.74,
        risk_level="HIGH",
        model_name="Random Forest",
    )
    db_session.add(prediction)
    db_session.commit()

    saved_prediction = db_session.query(AttritionPrediction).first()
    assert saved_prediction is not None
    assert saved_prediction.employee_id == employee.id


def test_recommendation_references_department(db_session: Session) -> None:
    department = Department(name="Marketing", description="Marketing functions")
    db_session.add(department)
    db_session.commit()

    recommendation = Recommendation(
        department_id=department.id,
        recommendation_type="HIRE",
        recommendation_text="Increase hiring priority due to projected workforce gap.",
        priority="HIGH",
        recommended_employee_count=12,
    )
    db_session.add(recommendation)
    db_session.commit()

    saved_recommendation = db_session.query(Recommendation).first()
    assert saved_recommendation is not None
    assert saved_recommendation.department_id == department.id


def test_employee_schema_validation_works() -> None:
    with pytest.raises(ValidationError):
        EmployeeCreate(
            employee_id="EMP3001",
            name="Alex Jordan",
            department_id=1,
            job_role="Data Engineer",
            age=18,
            gender="M",
            experience_years=3,
            joining_date="2023-01-01",
            salary=-500,
            performance_score=85,
            satisfaction_score=7.2,
            employment_type="FULL_TIME",
            location="Boston",
            attrition_status="ACTIVE",
        )


def test_user_can_be_created(db_session: Session) -> None:
    user = User(
        username="hr_manager",
        email="manager@workforce.local",
        password_hash="hashed_password",
        role="HR_MANAGER",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    saved_user = db_session.query(User).filter(User.email == "manager@workforce.local").first()
    assert saved_user is not None
    assert saved_user.role == "HR_MANAGER"
