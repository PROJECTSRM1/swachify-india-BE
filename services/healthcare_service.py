from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException,status
from datetime import datetime

from sqlalchemy import text
from models.generated_models import (
    AmbulanceBooking,
    Appointments,
    DoctorProfile,
    MasterConsultationType,
    MasterDoctorSpecialization,
    MasterAmbulance,
    MasterAssistants,
    AvailableLabs,
    AvailablePharmacies,
    MasterHospital,
    UserRegistration,
)
from schemas.healthcare_schema import AmbulanceBookingCreateSchema, AppointmentCreateSchema, AppointmentResponseSchema, AvailableLabCreate,DoctorCreateSchema, IdNameSchema
from schemas.healthcare_schema import PaymentCreateSchema,AvailablePharmacyCreate
from models.generated_models import Payments, ServiceRequests,AvailablePharmacies

def map_appointment_response(a: Appointments) -> AppointmentResponseSchema:
    return AppointmentResponseSchema(
        id=a.id,
        user_id=a.user_id,
        appointment_time=a.appointment_time,

        consultation_type_id=a.consultation_type_id,
        doctor_id=a.doctor_id,
        doctor_specialization_id=a.doctor_specialization_id,
        ambulance_id=a.ambulance_id,
        assistant_id=a.assistant_id,
        labs_id=a.labs_id,
        pharmacies_id=a.pharmacies_id,

        consultation_type=(
            IdNameSchema(
                id=a.consultation_type.id,
                name=a.consultation_type.consultation_type
            ) if a.consultation_type else None
        ),

        doctor=(
            IdNameSchema(
                id=a.doctor.id,
                name=f"{a.doctor.user.first_name} {a.doctor.user.last_name}"
            ) if a.doctor and a.doctor.user else None
        ),

        doctor_specialization=(
            IdNameSchema(
                id=a.doctor_specialization.id,
                name=a.doctor_specialization.specialization_name
            ) if a.doctor_specialization else None
        ),

        ambulance=(
            IdNameSchema(
                id=a.ambulance.id,
                name=a.ambulance.vehicle_number
            ) if a.ambulance else None
        ),

        assistant=(
            IdNameSchema(
                id=a.assistant.id,
                name=a.assistant.name
            ) if a.assistant else None
        ),

        labs=(
            IdNameSchema(
                id=a.labs.id,
                name=a.labs.lab_name
            ) if a.labs else None
        ),

        pharmacies=(
            IdNameSchema(
                id=a.pharmacies.id,
                name=a.pharmacies.pharmacy_name
            ) if a.pharmacies else None
        ),

        hospital=(
            IdNameSchema(
                id=a.hospital.id,
                name=a.hospital.hospital_name
            ) if a.hospital else None
        ),

        required_ambulance=a.required_ambulance,
        required_assistant=a.required_assistant,
        pickup_time=a.pickup_time,
        status=a.status,
        call_booking_status=a.call_booking_status,
        is_active=a.is_active
    )

def create_healthcare_appointment(db: Session, data: AppointmentCreateSchema):
    user = db.query(UserRegistration).filter(
        UserRegistration.id == data.user_id,
        UserRegistration.is_active.is_(True)
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")

    appointment = Appointments(
        user_id=data.user_id,
        consultation_type_id=data.consultation_type_id,
        appointment_time=data.appointment_time,
        doctor_id=data.doctor_id,
        doctor_specialization_id=data.doctor_specialization_id,
        required_ambulance=data.required_ambulance,
        ambulance_id=data.ambulance_id if data.required_ambulance else None,
        pickup_time=data.pickup_time if data.required_ambulance else None,
        required_assistant=data.required_assistant,
        assistant_id=data.assistant_id if data.required_assistant else None,
        labs_id=data.labs_id,
        pharmacies_id=data.pharmacies_id,
        call_booking_status=data.call_booking_status,
        created_by=data.user_id,
        is_active=True
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return map_appointment_response(appointment)


def get_healthcare_appointments_by_user(db: Session, user_id: int):
    appointments = (
        db.query(Appointments)
        .options(
            joinedload(Appointments.consultation_type),
            joinedload(Appointments.doctor).joinedload(DoctorProfile.user),
            joinedload(Appointments.doctor_specialization),
            joinedload(Appointments.ambulance),
            joinedload(Appointments.assistants),     # ✅ PLURAL
            joinedload(Appointments.labs),
            joinedload(Appointments.pharmacies),
            joinedload(Appointments.hospital),
        )
        .filter(
            Appointments.user_id == user_id,
            Appointments.is_active.is_(True)
        )
        .order_by(Appointments.created_date.desc())
        .all()
    )

    return [map_appointment_response(a) for a in appointments]
def map_appointment_response(a: Appointments):
    return {
        "id": a.id,
        "user_id": a.user_id,
        "appointment_time": a.appointment_time,

        "consultation_type_id": a.consultation_type_id,
        "doctor_id": a.doctor_id,
        "doctor_specialization_id": a.doctor_specialization_id,
        "ambulance_id": a.ambulance_id,
        "assistant_id": a.assistants_id,
        "labs_id": a.labs_id,
        "pharmacies_id": a.pharmacies_id,

        "consultation_type": (
            {"id": a.consultation_type.id, "name": a.consultation_type.consultation_type}
            if a.consultation_type else None
        ),

        "doctor": (
            {"id": a.doctor.id, "name": f"{a.doctor.user.first_name} {a.doctor.user.last_name}"}
            if a.doctor and a.doctor.user else None
        ),

        "doctor_specialization": (
            {"id": a.doctor_specialization.id, "name": a.doctor_specialization.specialization_name}
            if a.doctor_specialization else None
        ),

        "ambulance": (
            {"id": a.ambulance.id, "name": a.ambulance.service_provider}
            if a.ambulance else None
        ),

        "assistant": (
            {"id": a.assistants.id, "name": a.assistants.name}
            if a.assistants else None
        ),

        "labs": (
            {"id": a.labs.id, "name": a.labs.lab_name}
            if a.labs else None
        ),

        "pharmacies": (
            {"id": a.pharmacies.id, "name": a.pharmacies.pharmacy_name}
            if a.pharmacies else None
        ),

        "hospital": (
            {"id": a.hospital.id, "name": a.hospital.hospital_name}
            if a.hospital else None
        ),

        "required_ambulance": a.required_ambulance,
        "required_assistant": a.required_assistant,
        "pickup_time": a.pickup_time,

        "status": a.status,
        "call_booking_status": a.call_booking_status,
        "is_active": a.is_active,
    }


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



def get_hospital_doctors_service(
    db: Session,
    hospital_id: int,
    specialization_id: int = -1
):
    """
    Calls DB function: fn_get_hospital_doctors(p_hospital_id, p_specialization_id)
    Returns list of doctors available in hospital
    """

    query = text("""
        SELECT *
        FROM fn_get_hospital_doctors(
            :hospital_id,
            :specialization_id
        )
    """)

    result = db.execute(
        query,
        {
            "hospital_id": hospital_id,
            "specialization_id": specialization_id
        }
    ).mappings().all()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No doctors found for this hospital"
        )

    return result

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
    query = text("""
        SELECT *
        FROM fn_get_available_hospitals()
    """)

    return db.execute(query).mappings().all()

def get_available_labs(db: Session):
    query = text("""
        SELECT *
        FROM public.vw_available_labs
    """)
    return db.execute(query).mappings().all()

def get_available_pharmacies_service(
    db: Session,
    filter_type: str
):
    query = text("""
        SELECT *
        FROM fn_get_available_pharmacies(:filter_type)
    """)

    return db.execute(
        query,
        {"filter_type": filter_type}
    ).mappings().all()

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

def get_available_labs_list_service(
    db: Session,
    filter_type: str
):
    query = text("""
        SELECT *
        FROM fn_get_available_labs_list(:filter_type)
    """)

    return db.execute(
        query,
        {"filter_type": filter_type}
    ).mappings().all()
    
#available_pharmacies    




def create_pharmacy_service(db: Session, payload: AvailablePharmacyCreate):

    # ✅ Validate created_by against registered users
    user = db.query(UserRegistration).filter(
        UserRegistration.id == payload.created_by
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid created_by: user not registered"
        )

    # ✅ Check duplicate pharmacy name
    existing = db.query(AvailablePharmacies).filter(
        AvailablePharmacies.pharmacy_name == payload.pharmacy_name
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pharmacy already exists"
        )

    pharmacy = AvailablePharmacies(**payload.dict())
    db.add(pharmacy)
    db.commit()
    db.refresh(pharmacy)
    return pharmacy
    
    
    
    
   


# # -------- GET ALL LABS --------
# def get_all_labs_service(db: Session):
#     return db.query(AvailableLabs).filter(AvailableLabs.is_active == True).all()


# -------- CREATE LAB --------
def create_lab_service(db: Session, lab_data: AvailableLabCreate):
    new_lab = AvailableLabs(**lab_data.dict())
    db.add(new_lab)
    db.commit()
    db.refresh(new_lab)
    return new_lab

from sqlalchemy import func

def get_appointments_by_doctor(
    db: Session,
    doctor_id: int
):
    data = (
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

    if not data:
        raise HTTPException(status_code=404, detail="No appointments found")

    return data
