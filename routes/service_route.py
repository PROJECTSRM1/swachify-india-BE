from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.service_schema import HomeServiceCreate
from core.database import get_db
from services.home_service import (
    create_home_service,
    get_all_home_services,
    get_home_service_by_id,
    delete_home_service
)

router = APIRouter(prefix="/home-service")

@router.post("/")
def create_service(db: Session = Depends(get_db), payload: HomeServiceCreate = None):
    return create_home_service(db, payload)

@router.get("/")
def fetch_all(db: Session = Depends(get_db)):
    return get_all_home_services(db)

@router.get("/{service_id}")
def fetch_by_id(service_id: int, db: Session = Depends(get_db)):
    service = get_home_service_by_id(db, service_id)
    if not service:
        return {"error": "Service not found"}
    return service

@router.delete("/{service_id}")
def delete(service_id: int, db: Session = Depends(get_db)):
    result = delete_home_service(db, service_id)
    if not result:
        return {"error": "Service not found"}
    return {"message": "Service deleted successfully"}
