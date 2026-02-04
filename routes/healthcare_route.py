from fastapi import APIRouter, Depends, Header, Path, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from core.dependencies import get_current_user
from models.generated_models import Appointments, DoctorProfile, UserRegistration
from schemas.healthcare_schema import (
    AmbulanceBookingCreateSchema,
    AmbulanceBookingResponseSchema,
    AppointmentCreateSchema,
    AppointmentResponseSchema,
    AvailableLabCreate,
    AvailableLabResponse,
    DoctorCreateSchema,
    DoctorResponseSchema,
    HospitalAmbulanceResponseSchema,
    PaymentCreateSchema,
    PaymentResponseSchema,
    AvailablePharmacyCreate,
    AvailablePharmacyResponse
    
    
)
from services.healthcare_service import (
    create_ambulance_booking,
    create_healthcare_appointment,
    create_lab_service,
    get_available_hospitals,
    get_available_labs,
    get_available_labs_list_service,
    get_available_pharmacies_service,
    get_healthcare_appointments_by_user,
    create_doctor_profile,
    get_available_doctors,
    get_hospital_ambulance_list,
    release_ambulance_booking,
    create_payment,
    get_doctor_bookings,
    get_my_bookings_by_user,
    create_pharmacy_service
)


router = APIRouter(prefix="/healthcare",tags=["Healthcare"])

@router.post("/doctors",response_model=DoctorResponseSchema,status_code=201)
def create_doctor(data: DoctorCreateSchema,db: Session = Depends(get_db)):
    return create_doctor_profile(db, data)

@router.post(
    "/appointments",
    response_model=AppointmentResponseSchema
)
def book_healthcare_appointment(
    payload: AppointmentCreateSchema,
    db: Session = Depends(get_db)
):
    return create_healthcare_appointment(db, payload)


@router.get(
    "/appointments/user/{user_id}",
    response_model=list[AppointmentResponseSchema]
)
def get_user_appointments(
    user_id: int,
    db: Session = Depends(get_db)
):
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

# @router.get("/available-labs")
# def fetch_available_labs(db: Session = Depends(get_db)):
#     return get_available_labs(db)

@router.get("/available-doctors")
def fetch_available_doctors(
    db: Session = Depends(get_db)
):
    return get_available_doctors(db)

@router.get("/available-pharmacies")
def fetch_available_pharmacies(
    filter_type: str = Query(
        "ALL",
        enum=[
            "ALL",
            "NEARBY",
            "RATING_4_5_PLUS",
            "HOME_DELIVERY"
        ],
        description="Filter pharmacies list"
    ),
    db: Session = Depends(get_db)
):
    return get_available_pharmacies_service(db, filter_type)

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
@router.get("/available-labs")
def fetch_available_labs_list(
    filter_type: str = Query(
        "ALL",
        enum=[
            "ALL",
            "NEARBY",
            "RATING_4_5_PLUS",
            "HOME_COLLECT"
        ],
        description="Filter labs list"
    ),
    db: Session = Depends(get_db)
):
    return get_available_labs_list_service(db, filter_type)

#avialbile_pharamcies



@router.post("/available-pharmacies")
def create_pharmacy_api(
    pharmacy_data: AvailablePharmacyCreate,
    db: Session = Depends(get_db)
):
    return create_pharmacy_service(db, pharmacy_data)



# -------- GET ALL --------
# @router.get("/healthcare", response_model=List[AvailableLabResponse])
# def get_labs(db: Session = Depends(get_db)):
#     return get_all_labs_service(db)

# -------- POST --------
@router.post("/available-labs", response_model=AvailableLabResponse)
def create_lab(
    lab: AvailableLabCreate,
    db: Session = Depends(get_db)
):
    return create_lab_service(db, lab)

from sqlalchemy import func
@router.get("/doctor/{doctor_id}")
def get_doctor_appointments_and_update_status(
    doctor_id: int,
    appointment_id: int | None = None,
    call_booking_status: str | None = None,
    db: Session = Depends(get_db)
):
    # 🔴 OPTIONAL UPDATE
    if appointment_id and call_booking_status:
        appointment = db.query(Appointments).filter(
            Appointments.id == appointment_id,
            Appointments.doctor_id == doctor_id,
            Appointments.is_active == True
        ).first()

        if appointment:
            appointment.call_booking_status = call_booking_status
            db.commit()

    # 🟢 FETCH
    rows = (
        db.query(
            Appointments.id.label("appointment_id"),
            func.concat(
                UserRegistration.first_name, " ", UserRegistration.last_name
            ).label("doctor_name"),
            Appointments.appointment_time,
            Appointments.call_booking_status
        )
        .join(DoctorProfile, DoctorProfile.id == Appointments.doctor_id)
        .join(UserRegistration, UserRegistration.id == DoctorProfile.user_id)
        .filter(
            Appointments.doctor_id == doctor_id,
            Appointments.is_active == True
        )
        .all()
    )

    # ✅ CONVERT TO JSON-SAFE FORMAT
    data = [
        {
            "appointment_id": r.appointment_id,
            "doctor_name": r.doctor_name,
            "appointment_time": r.appointment_time,
            "call_booking_status": r.call_booking_status
        }
        for r in rows
    ]

    return {
        "status": True,
        "data": data
    }


@router.patch("/appointments/{appointment_id}/call-booking-status")
def update_call_booking_status(
    appointment_id: int,
    call_booking_status: str,
    db: Session = Depends(get_db)
):
    allowed = ["Booked", "Consulted", "Medicines", "Lab tests"]

    if call_booking_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Allowed values: {allowed}"
        )

    appointment = db.query(Appointments).filter(
        Appointments.id == appointment_id,
        Appointments.is_active == True
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.call_booking_status = call_booking_status
    db.commit()

    return {
        "status": True,
        "message": "Call booking status updated"
    }
