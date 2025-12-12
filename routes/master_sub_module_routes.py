from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.master_sub_module_schema import (
    MasterSubModuleCreate,
    MasterSubModuleUpdate
)
from services.master_sub_module_service import MasterSubModuleService
from core.database import get_db   # Your DB dependency

router = APIRouter(
    prefix="/master/sub-modules",
    tags=["Master Sub Modules"]
)


# CREATE SUB MODULE
@router.post("/", response_model=dict, status_code=201)
def create_sub_module(payload: MasterSubModuleCreate, db: Session = Depends(get_db)):
    sub_module = MasterSubModuleService.create(db, payload)
    return {
        "message": "Sub Module created successfully",
        "data": sub_module
    }


# LIST ALL SUB MODULES
@router.get("/", status_code=200)
def list_all_sub_modules(db: Session = Depends(get_db)):
    return MasterSubModuleService.list_all(db)


# LIST SUB MODULES BY MODULE ID
@router.get("/module/{module_id}", status_code=200)
def list_submodules_by_module(module_id: int, db: Session = Depends(get_db)):
    return MasterSubModuleService.list_by_module(db, module_id)


# GET SUB MODULE BY ID
@router.get("/{sub_id}", status_code=200)
def get_sub_module(sub_id: int, db: Session = Depends(get_db)):
    return MasterSubModuleService.get_by_id(db, sub_id)


# UPDATE SUB MODULE
@router.put("/{sub_id}", status_code=200)
def update_sub_module(sub_id: int, payload: MasterSubModuleUpdate, db: Session = Depends(get_db)):
    updated_sub = MasterSubModuleService.update(db, sub_id, payload)
    return {
        "message": "Sub Module updated successfully",
        "data": updated_sub
    }


# DELETE SUB MODULE
@router.delete("/{sub_id}", status_code=200)
def delete_sub_module(sub_id: int, db: Session = Depends(get_db)):
    return MasterSubModuleService.delete(db, sub_id)
