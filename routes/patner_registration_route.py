from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.patner_registration_schema import (
    GeneralEducationRegistrationCreate,
    GeneralEducationRegistrationResponse,
    PatrnerRegistrationCreate,
    PartnerRegistrationResponse
)
from services.patner_registration_service import (
    create_general_education_registration_service,
    create_partner_registration_service
)

router = APIRouter(
    prefix="/partner-registration",
    tags=["Partner Registration"]
)


@router.post("/", response_model=PartnerRegistrationResponse)
def create_partner_registration(payload: PatrnerRegistrationCreate,db: Session = Depends(get_db)):
    return create_partner_registration_service(payload, db)

@router.post("/general-education", response_model=GeneralEducationRegistrationResponse)
def create_general_education(payload: GeneralEducationRegistrationCreate,db: Session = Depends(get_db)):
    return create_general_education_registration_service(payload, db)