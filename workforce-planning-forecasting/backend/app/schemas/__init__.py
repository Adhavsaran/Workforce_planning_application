from app.schemas.attrition_prediction import AttritionPredictionCreate, AttritionPredictionResponse, AttritionPredictionUpdate
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.schemas.forecast import ForecastCreate, ForecastGenerateRequest, ForecastResponse, ForecastUpdate
from app.schemas.recommendation import RecommendationCreate, RecommendationResponse, RecommendationUpdate
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.workforce_history import WorkforceHistoryCreate, WorkforceHistoryResponse, WorkforceHistoryUpdate

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "DepartmentCreate",
    "DepartmentUpdate",
    "DepartmentResponse",
    "EmployeeCreate",
    "EmployeeUpdate",
    "EmployeeResponse",
    "WorkforceHistoryCreate",
    "WorkforceHistoryUpdate",
    "WorkforceHistoryResponse",
    "ForecastCreate",
    "ForecastGenerateRequest",
    "ForecastUpdate",
    "ForecastResponse",
    "AttritionPredictionCreate",
    "AttritionPredictionUpdate",
    "AttritionPredictionResponse",
    "RecommendationCreate",
    "RecommendationUpdate",
    "RecommendationResponse",
]
