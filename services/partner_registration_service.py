from sqlalchemy.orm import Session
from models.generated_models import PartnerUsers, PartnerRegistration, GeneralEducationRegistration
from schemas.partner_registration_schema import (PartnerUserCreate,PartnerRegistrationCreate,GeneralEducationCreate)


def create_partner_user(db: Session, user: PartnerUserCreate):

    db_user = PartnerUsers(
        email=user.email,
        password=user.password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):

    return db.query(PartnerUsers).all()

def create_partner_registration(db: Session, data: PartnerRegistrationCreate):

    registration = PartnerRegistration(
        module_id=data.module_id,
        service_module_category_id=data.service_module_category_id,
        user_id=data.user_id
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
        phone_number=data.phone_number
    )

    db.add(education)
    db.commit()
    db.refresh(education)

    return education