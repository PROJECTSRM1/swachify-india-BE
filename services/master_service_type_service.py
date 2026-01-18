from sqlalchemy.orm import Session
from fastapi import HTTPException

# from models.master_service_type import MasterServiceType
from models.generated_models import MasterServiceType
from schemas.master_service_type_schema import (
    ServiceTypeCreate,
    ServiceTypeUpdate
)


def get_service_types(db: Session):
    return (
        db.query(MasterServiceType)
        .filter(MasterServiceType.is_active == True)
        .all()
    )


def get_service_type(db: Session, service_type_id: int):
    obj = db.get(MasterServiceType, service_type_id)

    if not obj or not obj.is_active:
        raise HTTPException(status_code=404, detail="Service type not found")

    return obj


def create_service_type(db: Session, data: ServiceTypeCreate):
    obj = MasterServiceType(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_service_type(db: Session, service_type_id: int, data: ServiceTypeUpdate):
    obj = db.get(MasterServiceType, service_type_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Service type not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_service_type(db: Session, service_type_id: int):
    obj = db.get(MasterServiceType, service_type_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Service type not found")

    if not obj.is_active:
        return {"message": "Service type already deleted"}

    obj.is_active = False
    db.commit()
    return {"message": "Service type deleted successfully"}
