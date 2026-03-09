from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from services.partner_registration_service import create_companies_registration, create_doctor_registration, create_general_education, create_hospital_registration, create_institution_school_college_registration, create_lab_registration, create_medical_store_registration, create_partner_user, create_partner_registration, create_student_registration, create_training_registration, create_my_food_registration
from schemas.partner_registration_schema import CompaniesRegistrationCreate, DoctorRegistrationCreate, HospitalRegistrationCreate, InstitutionSchoolCollegeRegistrationCreate, LabRegistrationCreate, MedicalStoreRegistrationCreate, PartnerUserCreate, PartnerRegistrationCreate, PartnerRegistrationResponse, PartnerUserResponse, GeneralEducationCreate, GeneralEducationResponse, StudentRegistrationCreate, TrainingRegistrationCreate, MyFoodRegistrationCreate

router = APIRouter(prefix="/partner-registration", tags=["Partner"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/users", response_model=PartnerUserResponse)
def create_user(user: PartnerUserCreate, db: Session = Depends(get_db)): return create_partner_user(db, user)

@router.post("/register", response_model=PartnerRegistrationResponse)
def register_partner(data: PartnerRegistrationCreate, db: Session = Depends(get_db)): return create_partner_registration(db, data)

@router.post("/general-education", response_model=GeneralEducationResponse)
def register_education(data: GeneralEducationCreate, db: Session = Depends(get_db)): return create_general_education(db, data)



@router.post("/institution-school-college")
def create_institution_school_college_api(
    payload: InstitutionSchoolCollegeRegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_institution_school_college_registration(db, payload)


@router.post("/student-registration")
def create_student_registration_api(
    payload: StudentRegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_student_registration(db, payload)

@router.post("/companies-registration")
def create_companies_registration_api(
    payload: CompaniesRegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_companies_registration(db, payload)



@router.post("/training-registration")
def create_training_registration_api(
    payload: TrainingRegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_training_registration(db, payload)



# ---------------- HOSPITAL ----------------
@router.post("/hospital-registration")
def create_hospital_api(
    payload: HospitalRegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_hospital_registration(db, payload)


# ---------------- LAB ----------------
@router.post("/lab-registration")
def create_lab_api(
    payload: LabRegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_lab_registration(db, payload)


# ---------------- MEDICAL STORE ----------------
@router.post("/medical-store-registration")
def create_medical_store_api(
    payload: MedicalStoreRegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_medical_store_registration(db, payload)


# ---------------- DOCTOR ----------------
@router.post("/doctor-registration")
def create_doctor_api(
    payload: DoctorRegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_doctor_registration(db, payload)


@router.post("/my-food-registration")
def create_my_food_registration_api(
    payload: MyFoodRegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_my_food_registration(db, payload)