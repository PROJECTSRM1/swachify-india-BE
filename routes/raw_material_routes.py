from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.raw_material_schema import RawMaterialCreate, RawMaterialResponse
from services.raw_material_service import (
    create_raw_material,
    get_all_raw_materials
)

router = APIRouter(prefix="/raw-material",tags=["Raw Material"])

@router.post("/",response_model=RawMaterialResponse,status_code=status.HTTP_201_CREATED)
def create_raw_material_api(payload: RawMaterialCreate,db: Session = Depends(get_db)):
    return create_raw_material(db=db, data=payload)


@router.get("/",response_model=List[RawMaterialResponse])
def get_raw_materials_api(
    db: Session = Depends(get_db)
):
    return get_all_raw_materials(db=db)
