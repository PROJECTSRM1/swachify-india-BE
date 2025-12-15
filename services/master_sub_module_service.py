from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.master_sub_module import MasterSubModule
from schemas.sub_module_schema import (
    SubModuleCreate,
    SubModuleUpdate
)


def get_sub_modules_service(db: Session, module_id: int):
    return (
        db.query(MasterSubModule)
        .filter(
            MasterSubModule.module_id == module_id,
            MasterSubModule.is_active == True
        )
        .all()
    )


def create_sub_module_service(db: Session, data: SubModuleCreate):
    obj = MasterSubModule(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_sub_module_service(
    db: Session,
    sub_module_id: int,
    data: SubModuleUpdate
):
    obj = db.get(MasterSubModule, sub_module_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Sub module not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_sub_module_service(db: Session, sub_module_id: int):
    obj = db.get(MasterSubModule, sub_module_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Sub module not found")

    if not obj.is_active:
        return {"message": "Sub module already deleted"}

    obj.is_active = False
    db.commit()

    return {"message": "Sub module deleted successfully"}
