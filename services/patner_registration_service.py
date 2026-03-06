from sqlalchemy.orm import Session
from models.generated_models import PartnerRegistration,GeneralEducationRegistration
from schemas.patner_registration_schema import PatrnerRegistrationCreate,PartnerRegistrationResponse,GeneralEducationRegistrationCreate,GeneralEducationRegistrationResponse

def create_partner_registration_service(payload: PatrnerRegistrationCreate,db: Session):
    partner = PartnerRegistration(
        module_id=payload.module_id,
        service_module_category_id=payload.service_module_category_id,
        email=payload.email,
        password=payload.password,
        phone_number=payload.phone_number,
        created_by=payload.created_by
    )
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

def create_general_education_registration_service(payload: GeneralEducationRegistrationCreate,db: Session):
    education = GeneralEducationRegistration(
        partner_registration_id=payload.partner_registration_id,
        name=payload.name,
        registration_type_id=payload.registration_type_id,
        pan_number=payload.pan_number,
        upload_fire_safety_certificate=payload.upload_fire_safety_certificate,
        address_pincode=payload.address_pincode,
        official_email=payload.official_email,
        gst_registration=payload.gst_registration,
        upload_gst_certificate=payload.upload_gst_certificate,
        bank_account=payload.bank_account,
        trade_license=payload.trade_license,
        noc=payload.noc,
        building_type_id=payload.building_type_id,
        upload_rental_agreement=payload.upload_rental_agreement,
        phone_number=payload.phone_number,
        verify_official_email=payload.verify_official_email,
        created_by=payload.created_by
    )
    db.add(education)
    db.commit()
    db.refresh(education)
    return education