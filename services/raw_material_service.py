from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.generated_models import RawMaterialDetails
from schemas.raw_material_schema import RawMaterialCreate


def create_raw_material(db: Session,data: RawMaterialCreate,user_id: int | None = None):
    raw_material = RawMaterialDetails(
        module_id=data.module_id,
        raw_material_type_id=data.raw_material_type_id,
        quantity=data.quantity,
        cost=data.cost,
        latitude=data.latitude,
        longitude=data.longitude,
        created_by=user_id
    )

    db.add(raw_material)
    db.commit()
    db.refresh(raw_material)

    return raw_material

def get_all_raw_materials(db: Session):
    materials = (
        db.query(RawMaterialDetails)
        .filter(RawMaterialDetails.is_active == True)
        .all()
    )

    if not materials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No raw material records found"
        )

    return materials
