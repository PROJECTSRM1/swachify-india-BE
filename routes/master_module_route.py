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
    MasterMechanicResponseSchema, HomeServiceBookingAddOnCreate, 
    HomeServiceBookingAddOnResponse, 
    HomeServicePaymentCreate,
      HomeServicePaymentResponse
)
from services.master_module_service import (
    create_booking_service_map,
    create_home_service_booking,
    create_home_service_booking_add_on,
    create_home_service_payment,
    create_master_mechanic,

    get_all_booking_service_maps,
    get_all_home_service_booking_add_ons,
    get_all_home_service_bookings,
    get_home_service_booking_summary,
    create_home_service_booking_add_on, 
    create_home_service_payment, 
    get_add_ons_by_booking_id,
      get_all_home_service_booking_add_ons, 
      get_all_home_service_payments, 
      get_payment_by_booking_id, 
      get_payment_by_user_id,


    get_home_service_booking_summary,
)

router = APIRouter(prefix="/api/home-service/bookings",tags=["Home Service Booking"])


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

# HomeServiceBookingAddOn

@router.post(
    "/add-ons",
    response_model=HomeServiceBookingAddOnResponse,
    status_code=201
)
def create_add_on(
    data: HomeServiceBookingAddOnCreate,
    db: Session = Depends(get_db)
):
    return create_home_service_booking_add_on(db, data)


@router.get(
    "/add-ons",
    response_model=list[HomeServiceBookingAddOnResponse]
)
def get_all_add_ons(
    db: Session = Depends(get_db)
):
    return get_all_home_service_booking_add_ons(db)


# @router.get(
#     "/add-ons/booking/{home_service_booking_id}",
#     response_model=list[HomeServiceBookingAddOnResponse]
# )
# def get_add_ons_by_booking(
#     home_service_booking_id: int,
#     db: Session = Depends(get_db)
# ):
#     return get_add_ons_by_booking_id(db, home_service_booking_id)


#HomeServicePayment

# -------- POST --------
@router.post(
    "-payments",
    response_model=HomeServicePaymentResponse
)
def create_payment(
    data: HomeServicePaymentCreate,
    db: Session = Depends(get_db)
):
    return create_home_service_payment(db, data)


# -------- GET ALL --------
@router.get(
    "-payments",
    response_model=list[HomeServicePaymentResponse]
)
def get_all_payments(
    db: Session = Depends(get_db)
):
    return get_all_home_service_payments(db)


# # -------- GET BY BOOKING ID --------
# @router.get(
#     "/booking/{booking_id}",
#     response_model=list[HomeServicePaymentResponse]
# )
# def get_payment_by_booking(
#     booking_id: int,
#     db: Session = Depends(get_db)
# ):
#     return get_payment_by_booking_id(db, booking_id)


# # -------- GET BY USER ID --------
# @router.get(
#     "/user/{user_id}",
#     response_model=list[HomeServicePaymentResponse]
# )
# def get_payment_by_user(
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     return get_payment_by_user_id(db, user_id)

@router.get("/home-service-booking-summary")
def fetch_home_service_booking_summary(
    db: Session = Depends(get_db)
):
    return {
        "status": True,
        "data": get_home_service_booking_summary(db)
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

