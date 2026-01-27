from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from models.generated_models import Appointments
from models.user_registration import UserRegistration
from models.generated_models import MasterAmbulance
from schemas.healthcare_schema import AppointmentCreateSchema


def create_healthcare_appointment(
    db: Session,
    data: AppointmentCreateSchema
):
    # 1️⃣ Validate User
    user = db.query(UserRegistration).filter(
        UserRegistration.id == data.user_id,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")

    # 2️⃣ Ambulance validation
    if data.required_ambulance:
        if not data.ambulance_id:
            raise HTTPException(status_code=400, detail="Ambulance ID is required")

        ambulance = db.query(MasterAmbulance).filter(
            MasterAmbulance.id == data.ambulance_id,
            MasterAmbulance.is_active == True,
            MasterAmbulance.availability_status == "Available"
        ).first()

        if not ambulance:
            raise HTTPException(status_code=400, detail="Ambulance not available")

    # 3️⃣ Save appointment
    appointment = Appointments(
        user_id=data.user_id,
        consultation_type=data.consultation_type,
        appointment_time=data.appointment_time,
        doctor_id=data.doctor_id,
        doctor_specialization_id=data.doctor_specialization_id,
        description=data.description,
        days_of_suffering=data.days_of_suffering,
        required_ambulance=data.required_ambulance,
        ambulance_id=data.ambulance_id if data.required_ambulance else None,
        pickup_time=data.pickup_time if data.required_ambulance else None,
        created_by=data.user_id,
        created_date=datetime.utcnow(),
        is_active=True
    )

    db.add(appointment)

    # 4️⃣ Update ambulance status
    if data.required_ambulance:
        ambulance.availability_status = "Booked"

    db.commit()
    db.refresh(appointment)

    return appointment


def get_healthcare_appointments_by_user(
    db: Session,
    user_id: int
):
    return db.query(Appointments).filter(
        Appointments.user_id == user_id,
        Appointments.is_active == True
    ).all()
