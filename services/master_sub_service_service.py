from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.generated_models import MasterSubService
from schemas.master_sub_service_schema import (SubServiceCreate,SubServiceUpdate)

def get_sub_services(db: Session, service_id: int):
    return (
        db.query(MasterSubService)
        .filter(
            MasterSubService.service_id == service_id,
            MasterSubService.is_active == True
        )
        .all()
    )

def create_sub_service(db: Session, data: SubServiceCreate):
    obj = MasterSubService(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_sub_service(db: Session,sub_service_id: int,data: SubServiceUpdate):
    obj = db.get(MasterSubService, sub_service_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Sub-service not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj

def delete_sub_service(db: Session, sub_service_id: int):
    obj = db.get(MasterSubService, sub_service_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Sub-service not found")

    if not obj.is_active:
        return {"message": "Sub-service already deleted"}

    obj.is_active = False
    db.commit()
    return {"message": "Sub-service deleted successfully"}
