from sqlalchemy.orm import Session
from fastapi import HTTPException
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
    """
    Create a new home service booking.
    
    Args:
        db: Database session
        data: HomeServiceCreate schema containing all service details
        user_id: The user ID (customer) creating the booking
    
    Returns:
        HomeService object with all details
    """
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
        
    """Get all active home services."""

    return db.query(HomeService).filter(HomeService.is_active == True).all()


def get_home_service(db: Session, service_id: int):
    """Get a specific home service by ID."""

    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")
    return obj


def update_home_service(db: Session, service_id: int, data: HomeServiceUpdate):

    """Update a home service booking."""

    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_home_service(db: Session, service_id: int):

    """Soft delete a home service (mark as inactive)."""
    
    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")

    obj.is_active = False
    db.commit()
    return {"message": "Service deactivated"}




