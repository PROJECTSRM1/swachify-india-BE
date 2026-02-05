from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from models.generated_models import HomeServiceBooking
from schemas.home_schema import (
    HomeServiceBookingCreateSchema,
    HomeServiceBookingResponseSchema,
    MasterMechanicCreateSchema,
    MasterMechanicResponseSchema
)
from services.master_module_service import (
    create_home_service_booking,
    create_master_mechanic,
    get_home_service_bookings
)

router = APIRouter(
    prefix="/home-service/bookings",
    tags=["Home Service Booking"]
)


@router.post("",response_model=HomeServiceBookingResponseSchema,status_code=201)
def create_booking(payload: HomeServiceBookingCreateSchema,db: Session = Depends(get_db)):
    booking = HomeServiceBooking(**payload.dict(),is_active=True)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get(
    "",
    response_model=List[HomeServiceBookingResponseSchema]
)
def fetch_bookings(
    id: Optional[int] = Query(None, description="Fetch booking by id"),
    db: Session = Depends(get_db)
):
    return get_home_service_bookings(
        db=db,
        booking_id=id
    )


@router.post(
    "/mechanics",
    response_model=MasterMechanicResponseSchema,
    status_code=201
)
def create_mechanic(
    payload: MasterMechanicCreateSchema,
    db: Session = Depends(get_db)
):
    return create_master_mechanic(db, payload)
