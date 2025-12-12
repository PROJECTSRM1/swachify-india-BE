from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.master_module_model import MasterModule
from schemas.master_module_schema import (
    MasterModuleCreate,
    MasterModuleUpdate
)


class MasterModuleService:

    # CREATE
    @staticmethod
    def create(db: Session, payload: MasterModuleCreate):
        module = MasterModule(**payload.dict())
        db.add(module)
        db.commit()
        db.refresh(module)
        return module

    # READ ALL
    @staticmethod
    def list_all(db: Session):
        return db.query(MasterModule).order_by(MasterModule.id).all()

    # READ ONE
    @staticmethod
    def get_by_id(db: Session, module_id: int):
        module = db.query(MasterModule).filter(MasterModule.id == module_id).first()

        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        return module

    # UPDATE
    @staticmethod
    def update(db: Session, module_id: int, payload: MasterModuleUpdate):
        module = db.query(MasterModule).filter(MasterModule.id == module_id).first()

        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        # Apply only fields that the user sent
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(module, key, value)

        db.commit()
        db.refresh(module)
        return module

    # DELETE
    @staticmethod
    def delete(db: Session, module_id: int):
        module = db.query(MasterModule).filter(MasterModule.id == module_id).first()

        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        db.delete(module)
        db.commit()
        return {"message": "Module deleted successfully"}
