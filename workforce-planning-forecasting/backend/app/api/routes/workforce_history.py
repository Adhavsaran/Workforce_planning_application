from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.workforce_history import WorkforceHistoryCreate, WorkforceHistoryUpdate
from app.services.workforce_history_service import (
    create_history_record,
    delete_history_record,
    get_history_by_id,
    get_history_summary,
    get_workforce_history,
    import_history_csv,
    update_history_record,
)

router = APIRouter(prefix="/api/workforce-history", tags=["Workforce History"])


@router.get("", summary="List workforce history")
def list_workforce_history(
    department_id: int | None = Query(default=None),
    year: int | None = Query(default=None),
    month: int | None = Query(default=None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_workforce_history(db, department_id=department_id, year=year, month=month, page=page, page_size=page_size)


@router.get("/summary", summary="Workforce history summary")
def workforce_history_summary(db: Session = Depends(get_db)):
    return get_history_summary(db)


@router.get("/{history_id}", summary="Get a specific workforce-history record")
def read_workforce_history(history_id: int, db: Session = Depends(get_db)):
    return get_history_by_id(db, history_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create workforce history")
def create_workforce_history_record(payload: WorkforceHistoryCreate, db: Session = Depends(get_db)):
    return create_history_record(db, payload)


@router.put("/{history_id}", summary="Update workforce history")
def update_workforce_history_record(history_id: int, payload: WorkforceHistoryUpdate, db: Session = Depends(get_db)):
    return update_history_record(db, history_id, payload)


@router.delete("/{history_id}", summary="Delete workforce history")
def delete_workforce_history_record(history_id: int, db: Session = Depends(get_db)):
    return delete_history_record(db, history_id)


@router.post("/import", summary="Import workforce history CSV")
def import_workforce_history(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return import_history_csv(db, file)
