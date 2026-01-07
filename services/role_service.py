from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.master_role import MasterRole

def validate_role(db: Session, role_id: int):
    role = db.query(MasterRole).filter(
        MasterRole.id == role_id,
        MasterRole.is_active == True
    ).first()

    if not role:
        raise HTTPException(
            status_code=400,
            detail="Invalid or inactive role_id"
        )

    return role
