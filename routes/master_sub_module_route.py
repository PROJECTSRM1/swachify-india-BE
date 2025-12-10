from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.sub_module_schema import (
    SubModuleCreate,
    SubModuleUpdate,
    SubModuleResponse,
)
from services.sub_module_service import (
    create_sub_module,
    get_all_sub_modules,
    get_sub_module,
    update_sub_module,
    delete_sub_module,
)

router = APIRouter(prefix="/sub-modules", tags=["Master Sub Module"])


@router.post("/", response_model=SubModuleResponse)
def create(data: SubModuleCreate, db: Session = Depends(get_db)):
    return create_sub_module(db, data)


@router.get("/", response_model=list[SubModuleResponse])
def list_all(db: Session = Depends(get_db)):
    return get_all_sub_modules(db)


@router.get("/{sub_module_id}", response_model=SubModuleResponse)
def get(sub_module_id: int, db: Session = Depends(get_db)):
    obj = get_sub_module(db, sub_module_id)
    if not obj:
        raise HTTPException(404, "Sub module not found")
    return obj


@router.put("/{sub_module_id}", response_model=SubModuleResponse)
def update(sub_module_id: int, data: SubModuleUpdate, db: Session = Depends(get_db)):
    obj = update_sub_module(db, sub_module_id, data)
    if not obj:
        raise HTTPException(404, "Sub module not found")
    return obj


@router.delete("/{sub_module_id}")
def delete(sub_module_id: int, db: Session = Depends(get_db)):
    ok = delete_sub_module(db, sub_module_id)
    if not ok:
        raise HTTPException(404, "Sub module not found")
    return {"message": "Deleted successfully"}
