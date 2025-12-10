from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db

from schemas.master_service_schema import (
    MasterServiceCreate,
    MasterServiceUpdate,
    MasterServiceResponse
)

from services.master_service_service import (
    get_all_services,
    get_service,
    create_service,
    update_service,
    delete_service
)

router = APIRouter(prefix="/master-service", tags=["Master Service"])


@router.get("/", response_model=list[MasterServiceResponse])
def all_services(db: Session = Depends(get_db)):
    return get_all_services(db)


@router.get("/{service_id}", response_model=MasterServiceResponse)
def get(service_id: int, db: Session = Depends(get_db)):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(404, "Service not found")
    return service


@router.post("/", response_model=MasterServiceResponse)
def create(data: MasterServiceCreate, db: Session = Depends(get_db)):
    return create_service(db, data)


@router.put("/{service_id}", response_model=MasterServiceResponse)
def update(service_id: int, data: MasterServiceUpdate, db: Session = Depends(get_db)):
    updated = update_service(db, service_id, data)
    if not updated:
        raise HTTPException(404, "Service not found")
    return updated


@router.delete("/{service_id}")
def delete(service_id: int, db: Session = Depends(get_db)):
    deleted = delete_service(db, service_id)
    if not deleted:
        raise HTTPException(404, "Service not found")
    return {"message": "Service deleted successfully"}
