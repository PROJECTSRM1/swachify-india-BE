from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from models.generated_models import HomeServiceBooking
from schemas.home_schema import (
    HomeServiceBookingCreateSchema,
    HomeServiceBookingMapCreateSchema,
    HomeServiceBookingMapResponseSchema,
    HomeServiceBookingResponseSchema,
    MasterMechanicCreateSchema,
    MasterMechanicResponseSchema
)
from services.master_module_service import (
    create_booking_service_map,
    create_home_service_booking,
    create_master_mechanic,
    get_all_booking_service_maps,
    get_all_home_service_bookings,
    get_home_service_booking_summary,
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


@router.post("/home-booking-service-map", response_model=HomeServiceBookingMapResponseSchema)
def create_booking_service(
    data: HomeServiceBookingMapCreateSchema,
    db: Session = Depends(get_db)
):
    return create_booking_service_map(db, data)



@router.get("/home-booking-service-map", response_model=list[HomeServiceBookingMapResponseSchema])
def get_all_booking_services(db: Session = Depends(get_db)):
    return get_all_booking_service_maps(db)