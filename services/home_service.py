from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.generated_models import HomeService
from schemas.home_schema import  HomeServiceCreate, HomeServiceUpdate
from core.constants import (
    BOOKING_STATUS_PENDING,
    STATUS_ASSIGNED,
    WORK_STATUS_ON_THE_WAY,
    WORK_STATUS_REACHED_LOCATION,
    WORK_STATUS_JOB_STARTED,
    WORK_STATUS_JOB_COMPLETED,
)



def create_home_service(db: Session, data: HomeServiceCreate, user_id: int):
  
    service = HomeService(
        **data.model_dump(exclude={"created_by"}),
        created_by=user_id,
        status_id=BOOKING_STATUS_PENDING,
        work_status_id=WORK_STATUS_ON_THE_WAY,
        is_active=True
    )

    db.add(service)
    db.commit()
    db.refresh(service)
    return service



def get_home_services(db: Session):
    return db.query(HomeService).filter(HomeService.is_active == True).all()


def get_home_service(db: Session, service_id: int):
    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")
    return obj


def update_home_service(db: Session, service_id: int, data: HomeServiceUpdate):
    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_home_service(db: Session, service_id: int):
    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")

    obj.is_active = False
    db.commit()
    return {"message": "Service deactivated"}








def update_home_service_rating(
    db: Session,
    service_id: int,
    rating: int
):
    service = (
        db.query(HomeService)
        .filter(
            HomeService.id == service_id,
            HomeService.is_active == True
        )
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Home service not found"
        )

    service.rating = rating
    db.commit()
    db.refresh(service)

    return {
        "message": "Rating updated successfully",
        "service_id": service.id,
        "rating": service.rating
    }
