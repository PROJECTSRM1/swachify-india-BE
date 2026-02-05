from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.home_schema import HomeServiceBookingAddOnCreate, HomeServiceBookingAddOnResponse, HomeServicePaymentCreate, HomeServicePaymentResponse
from services.master_module_service import create_home_service_booking_add_on, create_home_service_payment, get_add_ons_by_booking_id, get_all_home_service_booking_add_ons, get_all_home_service_payments, get_payment_by_booking_id, get_payment_by_user_id



router = APIRouter(
    prefix="/home-service-booking-add-ons",
    tags=["Home Service Booking Add Ons"]
)
#HomeServiceBookingAddOn

# -------- POST --------
@router.post(
    "/",
    response_model=HomeServiceBookingAddOnResponse
)
def create_add_on(
    data: HomeServiceBookingAddOnCreate,
    db: Session = Depends(get_db)
):
    return create_home_service_booking_add_on(db, data)


# -------- GET ALL --------
@router.get(
    "/",
    response_model=list[HomeServiceBookingAddOnResponse]
)
def get_all_add_ons(
    db: Session = Depends(get_db)
):
    return get_all_home_service_booking_add_ons(db)


# -------- GET BY BOOKING ID --------
@router.get(
    "/booking/{home_service_booking_id}",
    response_model=list[HomeServiceBookingAddOnResponse]
)
def get_add_ons_by_booking(
    home_service_booking_id: int,
    db: Session = Depends(get_db)
):
    return get_add_ons_by_booking_id(db, home_service_booking_id)

#HomeServicePayment

# -------- POST --------
@router.post(
    "/",
    response_model=HomeServicePaymentResponse
)
def create_payment(
    data: HomeServicePaymentCreate,
    db: Session = Depends(get_db)
):
    return create_home_service_payment(db, data)


# -------- GET ALL --------
@router.get(
    "/",
    response_model=list[HomeServicePaymentResponse]
)
def get_all_payments(
    db: Session = Depends(get_db)
):
    return get_all_home_service_payments(db)


# -------- GET BY BOOKING ID --------
@router.get(
    "/booking/{booking_id}",
    response_model=list[HomeServicePaymentResponse]
)
def get_payment_by_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    return get_payment_by_booking_id(db, booking_id)


# -------- GET BY USER ID --------
@router.get(
    "/user/{user_id}",
    response_model=list[HomeServicePaymentResponse]
)
def get_payment_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_payment_by_user_id(db, user_id)
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
