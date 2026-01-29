from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from sqlalchemy import text
from models.generated_models import AmbulanceBooking, Appointments, DoctorProfile,UserRegistration,MasterAmbulance, MasterDoctorSpecialization
from schemas.healthcare_schema import AmbulanceBookingCreateSchema, AppointmentCreateSchema,DoctorCreateSchema



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

#doctor

def create_doctor_profile(
    db: Session,
    data: DoctorCreateSchema
):
    # 1️⃣ Validate user
    user = db.query(UserRegistration).filter(
        UserRegistration.id == data.user_id,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # 2️⃣ Validate specialization
    specialization = db.query(MasterDoctorSpecialization).filter(
        MasterDoctorSpecialization.id == data.specialization_id,
        MasterDoctorSpecialization.is_active == True
    ).first()

    if not specialization:
        raise HTTPException(status_code=400, detail="Invalid specialization")

    # 3️⃣ Check doctor already exists
    existing_doctor = db.query(DoctorProfile).filter(
        DoctorProfile.user_id == data.user_id
    ).first()

    if existing_doctor:
        raise HTTPException(status_code=400, detail="Doctor profile already exists")

    # 4️⃣ Create doctor profile
    doctor = DoctorProfile(
        user_id=data.user_id,
        specialization_id=data.specialization_id,
        experience_years=data.experience_years,
        rating=data.rating,
        fees_per_hour=data.fees_per_hour,
        available_from=data.available_from,
        available_to=data.available_to,
        is_available=data.is_available,
        created_by=data.user_id
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor

def get_available_doctors(db):
    return db.query(DoctorProfile).filter(
        DoctorProfile.is_active == True,
        DoctorProfile.is_available == True
    ).all()

def get_hospital_ambulance_list(db: Session, hospital_id: int):
    if hospital_id == -1:
        query = text("SELECT * FROM vw_hospital_ambulance_list")
        return db.execute(query).mappings().all()
    else:
        query = text("""
            SELECT *
            FROM vw_hospital_ambulance_list
            WHERE hospital_id = :hospital_id
        """)
        return db.execute(
            query,
            {"hospital_id": hospital_id}
        ).mappings().all()
    


def create_ambulance_booking(
    db: Session,
    data: AmbulanceBookingCreateSchema
):
    # 1️⃣ Validate User (SAME AS CREATE DOCTOR)
    user = db.query(UserRegistration).filter(
        UserRegistration.id == data.user_id,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # 2️⃣ Validate Appointment
    appointment = db.query(Appointments).filter(
        Appointments.id == data.appointment_id,
        Appointments.is_active == True
    ).first()

    if not appointment:
        raise HTTPException(status_code=400, detail="Invalid appointment")

    # OPTIONAL (RECOMMENDED)
    if appointment.user_id != data.user_id:
        raise HTTPException(
            status_code=403,
            detail="Appointment does not belong to user"
        )

    # 3️⃣ Validate Ambulance
    ambulance = db.query(MasterAmbulance).filter(
        MasterAmbulance.id == data.ambulance_id,
        MasterAmbulance.is_active == True,
        MasterAmbulance.availability_status == "Available"
    ).first()

    if not ambulance:
        raise HTTPException(status_code=400, detail="Ambulance not available")

    # 4️⃣ Create Ambulance Booking
    booking = AmbulanceBooking(
        appointment_id=data.appointment_id,
        ambulance_id=data.ambulance_id,
        patient_name=data.patient_name,
        aadhar_number=data.aadhar_number,
        created_by=data.user_id,   # ✅ SAME STYLE AS CREATE DOCTOR
        is_active=True
    )

    db.add(booking)

    # 5️⃣ Update Ambulance Status
    ambulance.availability_status = "Booked"

    db.commit()
    db.refresh(booking)

    return {
        "id": booking.id,
        "appointment_id": booking.appointment_id,
        "ambulance_id": booking.ambulance_id,
        "patient_name": booking.patient_name,
        "aadhar_number": booking.aadhar_number,
        "is_active": booking.is_active,
        "service_provider": ambulance.service_provider,
        "contact_number": ambulance.contact_number
    }

def release_ambulance_booking(
    db: Session,
    booking_id: int
):
    # 1️⃣ Fetch active booking
    booking = db.query(AmbulanceBooking).filter(
        AmbulanceBooking.id == booking_id,
        AmbulanceBooking.is_active == True
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Active ambulance booking not found"
        )

    # 2️⃣ Fetch ambulance
    ambulance = db.query(MasterAmbulance).filter(
        MasterAmbulance.id == booking.ambulance_id
    ).first()

    if not ambulance:
        raise HTTPException(
            status_code=404,
            detail="Ambulance not found"
        )

    # 3️⃣ Release ambulance
    ambulance.availability_status = "Available"

    # 4️⃣ Mark booking inactive
    booking.is_active = False
    booking.modified_date = datetime.utcnow()

    db.commit()

    return {
        "message": "Ambulance released successfully",
        "ambulance_id": ambulance.id,
        "booking_id": booking.id
    }