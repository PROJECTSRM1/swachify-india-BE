from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from models.generated_models import HomeService
from schemas.home_schema import HomeServiceCreate, HomeServiceUpdate
from core.constants import (
    BOOKING_STATUS_PENDING,
    WORK_STATUS_ON_THE_WAY,
)

# =====================================================
# UTILS
# =====================================================

def sanitize_fk(value: Optional[int]) -> Optional[int]:
    """
    Converts 0 or None → None
    Keeps valid positive integers
    """
    if value in (0, None):
        return None
    return value


def validate_fk(db: Session, model, value: Optional[int], field_name: str):
    """
    Optional FK validation
    Uncomment calls if you want strict FK validation
    """
    if value is None:
        return
    exists = db.query(model.id).filter(model.id == value).first()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name}"
        )

def create_home_service(db: Session, data: HomeServiceCreate, user_id: int):
    payload = data.model_dump()

    # -----------------------------
    # 1. Convert frontend 0 → None
    # -----------------------------
    for key, value in payload.items():
        if value == 0:
            payload[key] = None

    # -----------------------------
    # 2. REQUIRED FIELD SAFETY
    # -----------------------------

    # sub_module_id is NOT NULL in DB
    if payload.get("sub_module_id") is None:
        return {
            "success": False,
            "service_id": None,
            "message": "Invalid sub_module_id. Please select a valid service category."
        }

    # module_id safety
    if payload.get("module_id") is None:
        return {
            "success": False,
            "service_id": None,
            "message": "Invalid module_id."
        }

    # service_id safety
    if payload.get("service_id") is None:
        return {
            "success": False,
            "service_id": None,
            "message": "Invalid service_id."
        }

    # -----------------------------
    # 3. Remove system-controlled fields
    # -----------------------------
    payload.pop("created_by", None)
    payload.pop("status_id", None)
    payload.pop("work_status_id", None)
    payload.pop("is_active", None)

    # -----------------------------
    # 4. Safe DB insert
    # -----------------------------
    try:
        service = HomeService(
            **payload
        )
        service.created_by = user_id
        service.status_id = BOOKING_STATUS_PENDING
        service.work_status_id = WORK_STATUS_ON_THE_WAY
        service.is_active = True

        db.add(service)
        db.commit()
        db.refresh(service)

    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "service_id": None,
            "message": "Unable to create booking. Please try again."
        }

    return {
        "success": True,
        "message": "Booking created successfully",
        "service_id": service.id,
        "status_id": service.status_id,
        "work_status_id": service.work_status_id,
        "created_by": service.created_by
    }
# =====================================================
# READ
# =====================================================

def get_home_services(db: Session):
    return (
        db.query(HomeService)
        .filter(HomeService.is_active == True)
        .order_by(HomeService.created_date.desc())
        .all()
    )


def get_home_service(db: Session, service_id: int):
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
            detail="Service not found"
        )

    return service


# =====================================================
# UPDATE
# =====================================================

def update_home_service(db: Session, service_id: int, data: HomeServiceUpdate):

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
            detail="Service not found"
        )

    update_data = data.model_dump(exclude_unset=True)

    # sanitize FK values on update too
    for key, value in update_data.items():
        if key.endswith("_id"):
            value = sanitize_fk(value)
        setattr(service, key, value)

    db.commit()
    db.refresh(service)
    return service


# =====================================================
# DELETE (SOFT)
# =====================================================

def delete_home_service(db: Session, service_id: int):

    service = (
        db.query(HomeService)
        .filter(HomeService.id == service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    db.delete(service)
    db.commit()
   

    return {"message": "Service deleted successfully"}


# =====================================================
# RATING
# =====================================================

def update_home_service_rating(
    db: Session,
    service_id: int,
    rating: float
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


