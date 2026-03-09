from pydantic import BaseModel,field_validator
from typing import Optional
from datetime import datetime


class PartnerUserCreate(BaseModel):
    email: str
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("Passwords do not match")
        return v

class PartnerUserResponse(BaseModel):
    id: int
    email: str
    created_date: Optional[datetime]

    class Config:
        from_attributes = True


# -------------------------
# Partner Registration
# -------------------------

class PartnerRegistrationCreate(BaseModel):
    module_id: int
    service_module_category_id: int
    user_id: int


class PartnerRegistrationResponse(PartnerRegistrationCreate):
    id: int

    class Config:
        from_attributes = True


# -------------------------
# General Education
# -------------------------

class GeneralEducationCreate(BaseModel):

    partner_registration_id: int
    name: str
    registration_type_id: int
    pan_number: str
    upload_fire_safety_certificate: str
    address_pincode: str
    official_email: str
    gst_registration: Optional[bool] = None
    upload_gst_certificate: Optional[str] = None
    bank_account: Optional[str] = None
    trade_license: Optional[bool] = None
    noc: Optional[bool] = None
    building_type_id: Optional[int] = None
    upload_rental_agreement: Optional[str] = None
    phone_number: Optional[str] = None


class GeneralEducationResponse(GeneralEducationCreate):

    id: int

    class Config:
        from_attributes = True