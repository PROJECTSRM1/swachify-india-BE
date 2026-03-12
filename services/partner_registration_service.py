from fastapi import HTTPException
from sqlalchemy.orm import Session
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

    db_user = PartnerUsers(email=user.email, password=user.password)

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


def create_institution_school_college_registration(
    db: Session, payload: InstitutionSchoolCollegeRegistrationCreate
):

    user = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == payload.created_by,
            UserRegistration.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid created_by. User not found"
        )

    obj = InstitutionSchoolCollegeRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def create_student_registration(db: Session, payload: StudentRegistrationCreate):

    user = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == payload.created_by,
            UserRegistration.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=400, detail="Invalid created_by. User not found"
        )

    obj = StudentRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def create_companies_registration(db: Session, payload: CompaniesRegistrationCreate):

    user = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == payload.created_by,
            UserRegistration.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=400, detail="Invalid created_by. User not found"
        )

    obj = CompaniesRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def create_training_registration(db: Session, payload: TrainingRegistrationCreate):

    user = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == payload.created_by,
            UserRegistration.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=400, detail="Invalid created_by. User not found"
        )

    obj = TrainingRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# ---------------- HOSPITAL ----------------
def create_hospital_registration(db: Session, payload: HospitalRegistrationCreate):

    user = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == payload.created_by,
            UserRegistration.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid created_by user")

    obj = HospitalRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# ---------------- LAB ----------------
def create_lab_registration(db: Session, payload: LabRegistrationCreate):

    user = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == payload.created_by,
            UserRegistration.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid created_by user")

    obj = LabRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# ---------------- MEDICAL STORE ----------------
def create_medical_store_registration(
    db: Session, payload: MedicalStoreRegistrationCreate
):

    user = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == payload.created_by,
            UserRegistration.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid created_by user")

    obj = MedicalStoreRegistration(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# ---------------- DOCTOR ----------------
def create_doctor_registration(db: Session, payload: DoctorRegistrationCreate):

    user = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == payload.created_by,
            UserRegistration.is_active == True,
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
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == payload.created_by,
            UserRegistration.is_active == True,
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
