from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.master_module_schema import (
    MasterModuleCreate,
    MasterModuleUpdate,
    MasterModuleResponse
)

from schemas.master_sub_module_schema import (
    MasterSubModuleCreate,
    MasterSubModuleUpdate,
    MasterSubModuleResponse
)

from services.master_module_service import MasterModuleService
from services.master_sub_module_service import MasterSubModuleService


router = APIRouter(prefix="/master", tags=["Master"])


# ------------------------------------------------
#               MASTER MODULE CRUD
# ------------------------------------------------

@router.post("/module", response_model=MasterModuleResponse)
def create_module(payload: MasterModuleCreate, db: Session = Depends(get_db)):
    return MasterModuleService.create(db, payload)


@router.get("/module", response_model=list[MasterModuleResponse])
def get_modules(db: Session = Depends(get_db)):
    return MasterModuleService.list_all(db)


@router.get("/module/{module_id}", response_model=MasterModuleResponse)
def get_single_module(module_id: int, db: Session = Depends(get_db)):
    return MasterModuleService.get_by_id(db, module_id)


@router.put("/module/{module_id}", response_model=MasterModuleResponse)
def update_module(module_id: int, payload: MasterModuleUpdate, db: Session = Depends(get_db)):
    return MasterModuleService.update(db, module_id, payload)


@router.delete("/module/{module_id}")
def delete_module(module_id: int, db: Session = Depends(get_db)):
    return MasterModuleService.delete(db, module_id)


# ------------------------------------------------
#            MASTER SUB MODULE CRUD
# ------------------------------------------------

@router.post("/sub-module", response_model=MasterSubModuleResponse)
def create_sub_module(payload: MasterSubModuleCreate, db: Session = Depends(get_db)):
    return MasterSubModuleService.create(db, payload)


@router.get("/sub-module/{module_id}", response_model=list[MasterSubModuleResponse])
def get_sub_modules(module_id: int, db: Session = Depends(get_db)):
    return MasterSubModuleService.list_by_module(db, module_id)


@router.get("/sub-module/detail/{sub_id}", response_model=MasterSubModuleResponse)
def get_single_submodule(sub_id: int, db: Session = Depends(get_db)):
    return MasterSubModuleService.get_by_id(db, sub_id)


@router.put("/sub-module/{sub_id}", response_model=MasterSubModuleResponse)
def update_sub_module(sub_id: int, payload: MasterSubModuleUpdate, db: Session = Depends(get_db)):
    return MasterSubModuleService.update(db, sub_id, payload)


@router.delete("/sub-module/{sub_id}")
def delete_sub_module(sub_id: int, db: Session = Depends(get_db)):
    return MasterSubModuleService.delete(db, sub_id)
