from sqlalchemy.orm import Session
from fastapi import HTTPException

# from models.master_module import MasterModule
from models.generated_models import MasterModule
from schemas.master_module_schema import (MasterModuleCreate,MasterModuleUpdate)

def get_modules_service(db: Session):
    return db.query(MasterModule).filter(
        MasterModule.is_active == True
    ).all()


def create_module_service(db: Session, data: MasterModuleCreate):
    obj = MasterModule(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_module_service(db: Session,module_id: int,data: MasterModuleUpdate):
    obj = db.get(MasterModule, module_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Module not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_module_service(db: Session, module_id: int):
    obj = db.get(MasterModule, module_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Module not found")

    if not obj.is_active:
        return {"message": "Module already deleted"}

    obj.is_active = False
    db.commit()
    db.refresh(obj)

    return {"message": "Module deleted successfully"}
