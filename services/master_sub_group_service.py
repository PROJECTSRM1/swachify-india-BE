from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.master_sub_group import MasterSubGroup
from schemas.master_sub_group_schema import (SubGroupCreate,SubGroupUpdate)



def get_sub_groups(db: Session, sub_service_id: int):
    return (
        db.query(MasterSubGroup)
        .filter(
            MasterSubGroup.sub_service_id == sub_service_id,
            MasterSubGroup.is_active == True
        )
        .all()
    )

def create_sub_group(db: Session, data: SubGroupCreate):
    obj = MasterSubGroup(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
def update_sub_group(
    db: Session,
    sub_group_id: int,
    data: SubGroupUpdate
):
    obj = db.get(MasterSubGroup, sub_group_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Sub group not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj
def delete_sub_group(db: Session, sub_group_id: int):
    obj = db.get(MasterSubGroup, sub_group_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Sub group not found")

    if not obj.is_active:
        return {"message": "Sub group already deleted"}

    obj.is_active = False
    db.commit()
    return {"message": "Sub group deleted successfully"}
