from fastapi import APIRouter, Depends, Header, Path, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from core.dependencies import get_current_user
from models.generated_models import UserRegistration
from schemas.healthcare_schema import (
    AmbulanceBookingCreateSchema,
    AmbulanceBookingResponseSchema,
    AppointmentCreateSchema,
    AppointmentResponseSchema,
    DoctorCreateSchema,
    DoctorResponseSchema,
    HospitalAmbulanceResponseSchema,
    PaymentCreateSchema,
    PaymentResponseSchema
    
)
from services.healthcare_service import (
    create_ambulance_booking,
    create_healthcare_appointment,
    get_available_hospitals,
    get_available_labs,
    get_available_pharmacies,
    get_healthcare_appointments_by_user,
    create_doctor_profile,
    get_available_doctors,
    get_hospital_ambulance_list,
    release_ambulance_booking,
    create_payment,
    get_doctor_bookings,
    get_my_bookings_by_user
)


router = APIRouter(prefix="/healthcare",tags=["Healthcare"])

@router.post("/doctors",response_model=DoctorResponseSchema,status_code=201)
def create_doctor(data: DoctorCreateSchema,db: Session = Depends(get_db)):
    return create_doctor_profile(db, data)

@router.post("/appointments",response_model=AppointmentResponseSchema,status_code=201)
def book_healthcare_appointment(data: AppointmentCreateSchema,db: Session = Depends(get_db)):
    return create_healthcare_appointment(db, data)\
    
@router.get("/appointments/user/{user_id}",response_model=list[AppointmentResponseSchema])
def get_user_appointments(user_id: int,db: Session = Depends(get_db)):
    return get_healthcare_appointments_by_user(db, user_id)


# @router.get("/doctors/available",response_model=list[DoctorResponseSchema])
# def fetch_available_doctors(db: Session = Depends(get_db)):
#     return get_available_doctors(db)


@router.get("/available-ambulances")
def fetch_hospital_ambulances(hospital_id: int = -1,db: Session = Depends(get_db)):
    return get_hospital_ambulance_list(db, hospital_id)

@router.post("/ambulance-booking",response_model=AmbulanceBookingResponseSchema,status_code=201)
def book_ambulance(data: AmbulanceBookingCreateSchema,db: Session = Depends(get_db)):
    return create_ambulance_booking(db, data)

@router.put("/ambulance-booking/{booking_id}/release")
def release_ambulance(booking_id: int,db: Session = Depends(get_db)):
    return release_ambulance_booking(db, booking_id)

@router.get("/available-hospitals")
def fetch_available_hospitals(db: Session = Depends(get_db)):
    return get_available_hospitals(db)

@router.get("/available-labs")
def fetch_available_labs(db: Session = Depends(get_db)):
    return get_available_labs(db)

@router.get("/available-doctors")
def fetch_available_doctors(
    db: Session = Depends(get_db)
):
    return get_available_doctors(db)

@router.get("/available-pharmacies")
def fetch_available_pharmacies(db: Session = Depends(get_db)):
    return get_available_pharmacies(db)

@router.post(
    "/payments",
    response_model=PaymentResponseSchema,
    status_code=201
)
def make_payment(
    data: PaymentCreateSchema,
    db: Session = Depends(get_db)
):
    return create_payment(db, data)

@router.get("/bookings/view-my-bookings/{user_id}")
def fetch_doctor_bookings(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    return get_doctor_bookings(db, user_id)
