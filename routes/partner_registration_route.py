from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from services.partner_registration_service import create_general_education, create_partner_user, create_partner_registration
from schemas.partner_registration_schema import PartnerUserCreate, PartnerRegistrationCreate, PartnerRegistrationResponse, PartnerUserResponse, GeneralEducationCreate, GeneralEducationResponse

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