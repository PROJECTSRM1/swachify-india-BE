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

    # Validate partner registration
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

    obj = InstitutionSchoolCollegeRegistration(**payload.model_dump())

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


# ============================================================
# GET FUNCTIONS (ALL OR BY ID)
# ============================================================

def get_companies(db: Session, company_id: int | None = None):

    if company_id:
        company = db.query(CompaniesRegistration).filter(
            CompaniesRegistration.id == company_id
        ).first()

        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        return company

    return db.query(CompaniesRegistration).all()


def get_training(db: Session, training_id: int | None = None):

    if training_id:
        training = db.query(TrainingRegistration).filter(
            TrainingRegistration.id == training_id
        ).first()

        if not training:
            raise HTTPException(status_code=404, detail="Training not found")

        return training

    return db.query(TrainingRegistration).all()


def get_hospitals(db: Session, hospital_id: int | None = None):

    if hospital_id:
        hospital = db.query(HospitalRegistration).filter(
            HospitalRegistration.id == hospital_id
        ).first()

        if not hospital:
            raise HTTPException(status_code=404, detail="Hospital not found")

        return hospital

    return db.query(HospitalRegistration).all()


def get_labs(db: Session, lab_id: int | None = None):

    if lab_id:
        lab = db.query(LabRegistration).filter(
            LabRegistration.id == lab_id
        ).first()

        if not lab:
            raise HTTPException(status_code=404, detail="Lab not found")

        return lab

    return db.query(LabRegistration).all()


def get_medical_stores(db: Session, store_id: int | None = None):

    if store_id:
        store = db.query(MedicalStoreRegistration).filter(
            MedicalStoreRegistration.id == store_id
        ).first()

        if not store:
            raise HTTPException(status_code=404, detail="Medical store not found")

        return store

    return db.query(MedicalStoreRegistration).all()


def get_doctors(db: Session, doctor_id: int | None = None):

    if doctor_id:
        doctor = db.query(DoctorRegistration).filter(
            DoctorRegistration.id == doctor_id
        ).first()

        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        return doctor

    return db.query(DoctorRegistration).all()


def get_students(db: Session, student_id: int | None = None):

    if student_id:
        student = db.query(StudentRegistration).filter(
            StudentRegistration.id == student_id
        ).first()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return student

    return db.query(StudentRegistration).all()


def get_general_education(db: Session, edu_id: int | None = None):

    if edu_id:
        edu = db.query(GeneralEducationRegistration).filter(
            GeneralEducationRegistration.id == edu_id
        ).first()

        if not edu:
            raise HTTPException(status_code=404, detail="Education not found")

        return edu

    return db.query(GeneralEducationRegistration).all()


def get_my_food(db: Session, food_id: int | None = None):

    if food_id:
        food = db.query(MyFoodRegistration).filter(
            MyFoodRegistration.id == food_id
        ).first()

        if not food:
            raise HTTPException(status_code=404, detail="Food record not found")

        return food

    return db.query(MyFoodRegistration).all()