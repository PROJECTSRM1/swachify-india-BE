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