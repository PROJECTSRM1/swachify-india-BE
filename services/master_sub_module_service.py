from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.master_sub_module_model import MasterSubModule
from schemas.master_sub_module_schema import (
    MasterSubModuleCreate,MasterSubModuleUpdate
)


class MasterSubModuleService:

    # CREATE
    @staticmethod
    def create(db: Session, payload: MasterSubModuleCreate):
        sub = MasterSubModule(**payload.dict())
        db.add(sub)
        db.commit()
        db.refresh(sub)
        return sub

    # READ ALL BY MODULE ID
    @staticmethod
    def list_by_module(db: Session, module_id: int):
        return db.query(MasterSubModule).filter(
            MasterSubModule.module_id == module_id
        ).all()

    # READ ALL RECORDS
    @staticmethod
    def list_all(db: Session):
        return db.query(MasterSubModule).order_by(MasterSubModule.id).all()

    # READ SINGLE SUBMODULE
    @staticmethod
    def get_by_id(db: Session, sub_id: int):
        sub = db.query(MasterSubModule).filter(
            MasterSubModule.id == sub_id
        ).first()

        if not sub:
            raise HTTPException(status_code=404, detail="Sub Module not found")

        return sub

    # UPDATE SUBMODULE
    @staticmethod
    def update(db: Session, sub_id: int, payload: MasterSubModuleUpdate):
        sub = db.query(MasterSubModule).filter(
            MasterSubModule.id == sub_id
        ).first()

        if not sub:
            raise HTTPException(status_code=404, detail="Sub Module not found")

        # Update only fields provided in payload
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(sub, key, value)

        db.commit()
        db.refresh(sub)
        return sub

    # DELETE SUBMODULE
    @staticmethod
    def delete(db: Session, sub_id: int):
        sub = db.query(MasterSubModule).filter(
            MasterSubModule.id == sub_id
        ).first()

        if not sub:
            raise HTTPException(status_code=404, detail="Sub Module not found")

        db.delete(sub)
        db.commit()
        return {"message": "Sub Module deleted successfully"}
