from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analytics import router as analytics_router
from app.api.routes.departments import router as departments_router
from app.api.routes.employees import router as employees_router
from app.api.routes.forecast import router as forecast_router
from app.api.routes.health import router as health_router
from app.api.routes.workforce_history import router as workforce_history_router
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(
    title="Workforce Planning & Forecasting Tool",
    version="0.1.0",
    description="HR decision-support platform for workforce planning and forecasting.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(employees_router)
app.include_router(departments_router)
app.include_router(workforce_history_router)
app.include_router(forecast_router)
app.include_router(analytics_router)


@app.get("/")
def read_root():
    return {"message": "Workforce Planning & Forecasting Tool"}
