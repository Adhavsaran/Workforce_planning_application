from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.attrition_prediction import AttritionPrediction
from app.models.department import Department
from app.models.employee import Employee
from app.models.forecast import Forecast
from app.models.recommendation import Recommendation
from app.models.user import User
from app.models.workforce_history import WorkforceHistory
