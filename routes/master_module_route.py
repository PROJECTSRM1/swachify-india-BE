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
    get_all_home_service_bookings,
    get_home_service_booking_summary
)

router = APIRouter(prefix="/home-service/bookings",tags=["Home Service Booking"])


@router.post("",response_model=HomeServiceBookingResponseSchema,status_code=201)
def create_booking(payload: HomeServiceBookingCreateSchema,db: Session = Depends(get_db)):
    return create_home_service_booking(db, payload)

@router.get("/all")
def fetch_all_home_service_bookings(db: Session = Depends(get_db)):
    return {
        "status": True,
        "data": get_all_home_service_bookings(db)
    }


@router.post("/mechanics",response_model=MasterMechanicResponseSchema,status_code=201)
def create_mechanic(payload: MasterMechanicCreateSchema,db: Session = Depends(get_db)):
    return create_master_mechanic(db, payload)

# ======================================================
# HOME SERVICE BOOKING SUMMARY (VIEW)
# ======================================================
@router.get("/home-service-bookings-summary")
def fetch_home_service_booking_summary(
    status_id: int = Query(
        -1,
        description="Pass status_id or -1 for all"
    ),
    db: Session = Depends(get_db)
):
    return {
        "status": True,
        "data": get_home_service_booking_summary(
            db=db,
            status_id=status_id
        )
    }