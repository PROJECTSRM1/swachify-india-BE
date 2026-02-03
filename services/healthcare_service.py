from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from datetime import datetime

from sqlalchemy import text
from models.generated_models import AmbulanceBooking, Appointments, DoctorProfile, MasterConsultationType, MasterHospital,UserRegistration,MasterAmbulance, MasterDoctorSpecialization
from schemas.healthcare_schema import AmbulanceBookingCreateSchema, AppointmentCreateSchema,DoctorCreateSchema
from schemas.healthcare_schema import PaymentCreateSchema
from models.generated_models import Payments, ServiceRequests


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

    # 2️⃣ Validate Ambulance
    ambulance = None
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

    # 3️⃣ Validate Assistant
    if data.required_assistant and not data.assistant_id:
        raise HTTPException(status_code=400, detail="Assistant ID is required")

    # 4️⃣ Create Appointment
    appointment = Appointments(
        user_id=data.user_id,
        consultation_type_id=data.consultation_type_id,
        appointment_time=data.appointment_time,

        doctor_id=data.doctor_id,
        doctor_specialization_id=data.doctor_specialization_id,
        description=data.description,
        days_of_suffering=data.days_of_suffering,
        health_insurance=data.health_insurance,

        required_ambulance=data.required_ambulance,
        ambulance_id=data.ambulance_id if data.required_ambulance else None,
        pickup_time=data.pickup_time if data.required_ambulance else None,

        required_assistant=data.required_assistant,
        assistant_id=data.assistant_id if data.required_assistant else None,

        labs_id=data.labs_id,
        pharmacies_id=data.pharmacies_id,

        created_by=data.user_id,
        created_date=datetime.utcnow(),
        is_active=True
    )

    db.add(appointment)

    # 5️⃣ Update Ambulance Status
    if ambulance:
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
        raise HTTPException(status_code=400, detail="Invalid user")

    # 2️⃣ Check doctor profile already exists
    existing = db.query(DoctorProfile).filter(
        DoctorProfile.user_id == data.user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Doctor profile already exists for this user"
        )

    # 3️⃣ Validate specialization
    specialization = db.query(MasterDoctorSpecialization).filter(
        MasterDoctorSpecialization.id == data.specialization_id,
        MasterDoctorSpecialization.is_active == True
    ).first()

    if not specialization:
        raise HTTPException(status_code=400, detail="Invalid specialization")

    # 4️⃣ Validate hospital (optional)
    if data.hospital_id:
        hospital = db.query(MasterHospital).filter(
            MasterHospital.id == data.hospital_id,
            MasterHospital.is_active == True
        ).first()

        if not hospital:
            raise HTTPException(status_code=400, detail="Invalid hospital")

    # 5️⃣ Validate consultation type (optional)
    if data.consultation_type_id:
        consultation_type = db.query(MasterConsultationType).filter(
            MasterConsultationType.id == data.consultation_type_id,
            MasterConsultationType.is_active == True
        ).first()

        if not consultation_type:
            raise HTTPException(status_code=400, detail="Invalid consultation type")

    # 6️⃣ Validate availability time
    if data.available_from and data.available_to:
        if data.available_to <= data.available_from:
            raise HTTPException(
                status_code=400,
                detail="available_to must be after available_from"
            )

    # 7️⃣ Create doctor profile
    doctor = DoctorProfile(
        user_id=data.user_id,
        specialization_id=data.specialization_id,
        experience_years=data.experience_years,
        rating=data.rating,
        fees_per_hour=data.fees_per_hour,
        available_from=data.available_from,
        available_to=data.available_to,
        is_available=data.is_available,
        hospital_id=data.hospital_id,
        consultation_type_id=data.consultation_type_id,
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
        query = text("SELECT * FROM vw_nearby_ambulance_list")
        return db.execute(query).mappings().all()
    else:
        query = text("""
            SELECT *
            FROM vw_nearby_ambulance_list
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


def get_available_hospitals(db: Session):
    query = text(""" SELECT *FROM fn_get_available_hospitals() """)

def get_available_labs(db: Session):
    query = text("""
        SELECT *
        FROM public.vw_available_labs
    """)
    return db.execute(query).mappings().all()


def get_available_pharmacies(db: Session):
    query = text("SELECT * FROM public.vw_available_pharmacies")
    return db.execute(query).mappings().all()



def get_available_doctors(db: Session):
    query = text("""
        SELECT *
        FROM fn_get_available_doctors(:specialization_id)
    """)
    result = db.execute(
        query,
        {"specialization_id": -1}
    )
    return result.mappings().all()


# =======================
# PAYMENTS SERVICE
# =======================

def create_payment(
    db: Session,
    data: PaymentCreateSchema
):
    # 1️⃣ Validate User
    user = db.query(UserRegistration).filter(
        UserRegistration.id == data.user_id,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user"
        )

    # 2️⃣ Validate Service Request (NO is_active column)
    service_request = db.query(ServiceRequests).filter(
        ServiceRequests.id == data.service_request_id
    ).first()

    if not service_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid service request"
        )

    # 3️⃣ Create Payment
    payment = Payments(
        service_request_id=data.service_request_id,
        user_id=data.user_id,
        amount=data.amount,
        payment_method=data.payment_method,
        appointment_id=data.appointment_id,
        transaction_id=data.transaction_id,
        remarks=data.remarks,
        payment_status="PENDING",
        created_by=data.user_id,
        created_date=datetime.utcnow(),
        is_active=True
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment

   
  # ======================================================
# MY BOOKINGS (VIEW: vw_my_bookings)
# ======================================================

def get_my_bookings_by_user(db: Session, user_id: int):
    query = text("""
        SELECT *
        FROM vw_my_bookings
        WHERE user_id = :user_id
    """)
    return db.execute(
        query,
        {"user_id": user_id}
    ).mappings().all()


def get_doctor_bookings(db: Session, user_id: int):
    query = text("""
        SELECT *
        FROM vw_my_bookings
        WHERE user_id = :user_id
          AND service_type = 'DOCTOR'
    """)
    return db.execute(
        query,
        {"user_id": user_id}
    ).mappings().all()


