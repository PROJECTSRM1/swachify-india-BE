from fastapi import HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from models.generated_models import (
    CompaniesRegistration,
    DoctorRegistration,
    HospitalRegistration,
    InstitutionSchoolCollegeRegistration,
    LabRegistration,
    MedicalStoreRegistration,
    PartnerUsers,
    PartnerRegistration,
    GeneralEducationRegistration,
    StudentRegistration,
    TrainingRegistration,
    UserRegistration,
    MyFoodRegistration,
)
from schemas.partner_registration_schema import (
    CompaniesRegistrationCreate,
    DoctorRegistrationCreate,
    HospitalRegistrationCreate,
    InstitutionSchoolCollegeRegistrationCreate,
    LabRegistrationCreate,
    MedicalStoreRegistrationCreate,
    PartnerUserCreate,
    PartnerRegistrationCreate,
    GeneralEducationCreate,
    StudentRegistrationCreate,
    TrainingRegistrationCreate,
    MyFoodRegistrationCreate,
)



# -------------------------
# Create Partner User
# -------------------------

def create_partner_user(db: Session, user: PartnerUserCreate):

    existing_user = db.query(PartnerUsers).filter(
        PartnerUsers.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    db_user = PartnerUsers(
        email=user.email,
        password=user.password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# # -------------------------
# # Get All Users
# # -------------------------

# def get_users(db: Session):
#     return db.query(PartnerUsers).all()


# -------------------------
# Create Partner Registration
# -------------------------


def create_partner_registration(db: Session, data: PartnerRegistrationCreate):

    # Check if user exists
    user = db.query(PartnerUsers).filter(
        PartnerUsers.id == data.user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check duplicate registration
    existing = db.query(PartnerRegistration).filter(
        PartnerRegistration.user_id == data.user_id,
        PartnerRegistration.module_id == data.module_id,
        PartnerRegistration.service_module_category_id == data.service_module_category_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Partner already registered for this module and category"
        )

    registration = PartnerRegistration(
        module_id=data.module_id,
        service_module_category_id=data.service_module_category_id,
        user_id=data.user_id,
    )

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return registration


def create_general_education(db: Session, data: GeneralEducationCreate):

    education = GeneralEducationRegistration(
        partner_registration_id=data.partner_registration_id,
        name=data.name,
        registration_type_id=data.registration_type_id,
        pan_number=data.pan_number,
        upload_fire_safety_certificate=data.upload_fire_safety_certificate,
        address_pincode=data.address_pincode,
        official_email=data.official_email,
        gst_registration=data.gst_registration,
        upload_gst_certificate=data.upload_gst_certificate,
        bank_account=data.bank_account,
        trade_license=data.trade_license,
        noc=data.noc,
        building_type_id=data.building_type_id,
        upload_rental_agreement=data.upload_rental_agreement,
        phone_number=data.phone_number,
        verify_official_email=data.verify_official_email,
        created_by=data.created_by
    )

    db.add(education)
    db.commit()
    db.refresh(education)

    return education

def convert_percentage(value):
    if value is None:
        return None
    return Decimal(value) / Decimal(100)

def create_institution_school_college_registration(
    db: Session, payload: InstitutionSchoolCollegeRegistrationCreate
):

    partner = (
        db.query(PartnerRegistration)
        .filter(
            PartnerRegistration.id == payload.partner_registration_id,
            PartnerRegistration.is_active == True,
        )
        .first()
    )

    if not partner:
        raise HTTPException(
            status_code=400,
            detail="Invalid partner_registration_id"
        )

    data = payload.model_dump()

    # convert percentage fields to fit Numeric(3,2)
    percentage_fields = [
        "placement_year_1",
        "placement_year_2",
        "placement_year_3",
        "year_1_10th_result",
        "year_2_10th_result",
        "year_3_10th_result",
        "performance_pass_percentage_year1",
        "performance_pass_percentage_year2",
        "performance_pass_percentage_year3",
    ]

    for field in percentage_fields:
        if field in data and data[field] is not None:
            data[field] = convert_percentage(data[field])

    obj = InstitutionSchoolCollegeRegistration(**data)

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def create_student_registration(db: Session, payload: StudentRegistrationCreate):

    partner = (
        db.query(PartnerRegistration)
        .filter(
            PartnerRegistration.id == payload.partner_registration_id,
            PartnerRegistration.is_active == True
        )
        .first()
    )

    if not partner:
        raise HTTPException(
            status_code=400,
            detail="Invalid partner_registration_id. Partner not found"
        )

    obj = StudentRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def create_companies_registration(db: Session, payload: CompaniesRegistrationCreate):

    partner = (
        db.query(PartnerRegistration)
        .filter(
            PartnerRegistration.id == payload.created_by,
            PartnerRegistration.is_active == True
        )
        .first()
    )

    if not partner:
        raise HTTPException(
            status_code=400,
            detail="Invalid created_by. Partner not found"
        )

    obj = CompaniesRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def create_training_registration(db: Session, payload: TrainingRegistrationCreate):

    partner = (
        db.query(PartnerRegistration)
        .filter(
            PartnerRegistration.id == payload.created_by,
            PartnerRegistration.is_active == True
        )
        .first()
    )

    if not partner:
        raise HTTPException(
            status_code=400,
            detail="Invalid created_by. Partner not found"
        )

    obj = TrainingRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def create_hospital_registration(
    db: Session,
    payload: HospitalRegistrationCreate
):

    partner = (
        db.query(PartnerRegistration)
        .filter(
            PartnerRegistration.id == payload.created_by,
            PartnerRegistration.is_active == True
        )
        .first()
    )

    if not partner:
        raise HTTPException(
            status_code=400,
            detail="Invalid created_by. Partner not found"
        )

    obj = HospitalRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj

def create_lab_registration(db: Session, payload: LabRegistrationCreate):

    partner = (
        db.query(PartnerRegistration)
        .filter(
            PartnerRegistration.id == payload.created_by,
            PartnerRegistration.is_active == True
   
        )
        .first()
    )

    if not partner:
        raise HTTPException(
            status_code=400,
            detail="Invalid created_by. Partner not found"
        )

    # -------- VALIDATIONS FOR CHECK CONSTRAINTS --------

    if payload.drug_license_applicable and not payload.drug_license_number:
        raise HTTPException(
            status_code=400,
            detail="drug_license_number required when drug_license_applicable is true"
        )

    if payload.bmw_obtained and not payload.bmw_authorization_number:
        raise HTTPException(
            status_code=400,
            detail="bmw_authorization_number required when bmw_obtained is true"
        )

    if payload.fire_noc_obtained and not payload.fire_noc_number:
        raise HTTPException(
            status_code=400,
            detail="fire_noc_number required when fire_noc_obtained is true"
        )

    if payload.aerb_licence_applicable and not payload.aerb_license_number:
        raise HTTPException(
            status_code=400,
            detail="aerb_license_number required when aerb_licence_applicable is true"
        )

    if payload.pcpndt_certificate_applicable and not payload.pcpndt_certificate_number:
        raise HTTPException(
            status_code=400,
            detail="pcpndt_certificate_number required when pcpndt_certificate_applicable is true"
        )

    if payload.gst_registered and not payload.gst_number:
        raise HTTPException(
            status_code=400,
            detail="gst_number required when gst_registered is true"
        )

    # -------- INSERT --------

    obj = LabRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj

def create_medical_store_registration(
    db: Session,
    payload: MedicalStoreRegistrationCreate
):

    partner = (
        db.query(PartnerRegistration)
        .filter(
            PartnerRegistration.id == payload.created_by,
            PartnerRegistration.is_active == True
        )
        .first()
    )

    if not partner:
        raise HTTPException(
            status_code=400,
            detail="Invalid created_by. Partner not found"
        )

    obj = MedicalStoreRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# ---------------- DOCTOR ----------------
def create_doctor_registration(db: Session, payload: DoctorRegistrationCreate):

    user = (
        db.query(PartnerRegistration)
        .filter(
            PartnerRegistration.id == payload.created_by,
            PartnerRegistration.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid created_by user")

    obj = DoctorRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def create_my_food_registration(db: Session, payload: MyFoodRegistrationCreate):

    user = (
        db.query(PartnerRegistration)
        .filter(
            PartnerRegistration.id == payload.created_by,
            PartnerRegistration.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=400, detail="Invalid created_by. User not found"
        )

    obj = MyFoodRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj
