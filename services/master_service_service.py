from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.generated_models import MasterService
from schemas.master_service_schema import (
    MasterServiceCreate,
    MasterServiceUpdate
)


def get_services_by_sub_module(db: Session, sub_module_id: int):
    return (
        db.query(MasterService)
        .filter(
            MasterService.sub_module_id == sub_module_id,
            MasterService.is_active == True
        )
        .all()
    )


def create_service_service(db: Session, data: MasterServiceCreate):
    obj = MasterService(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_service_service(db: Session,service_id: int,data: MasterServiceUpdate):
    obj = db.get(MasterService, service_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Service not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_service_service(db: Session, service_id: int):
    obj = db.get(MasterService, service_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Service not found")

    if not obj.is_active:
        return {"message": "Service already deleted"}

    obj.is_active = False
    db.commit()

    return {"message": "Service deleted successfully"}
