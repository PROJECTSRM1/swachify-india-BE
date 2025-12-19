from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.home_service import HomeService
from schemas.home_schema import (
    HomeServiceCreate,
    HomeServiceUpdate
)


def get_home_services(db: Session):
    return db.query(HomeService).all()


def get_home_service(db: Session, home_service_id: int):
    obj = db.get(HomeService, home_service_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Home service not found")

    return obj


# def create_home_service(db: Session, data: HomeServiceCreate):
#     obj = HomeService(**data.model_dump())
#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return obj

def create_home_service(db: Session, data: HomeServiceCreate):
    obj = HomeService(
        **data.model_dump()
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def mark_payment_success(db: Session, home_service_id: int):
    obj = db.get(HomeService, home_service_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Home service not found")

    obj.payment_done = True
    db.commit()
    db.refresh(obj)
    return obj


def update_home_service(
    db: Session,
    home_service_id: int,
    data: HomeServiceUpdate
):
    obj = db.get(HomeService, home_service_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Home service not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_home_service(db: Session, home_service_id: int):
    obj = db.get(HomeService, home_service_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Home service not found")

    db.delete(obj)
    db.commit()

    return {"message": "Home service deleted successfully"}
