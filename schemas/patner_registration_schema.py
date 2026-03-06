from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class PatrnerRegistrationCreate(BaseModel):
    module_id:int
    service_module_category_id:int
    email:EmailStr
    password:str
    phone_number:str
    created_by:Optional[int]=None


class PartnerRegistrationResponse(BaseModel):
    id: int
    module_id: int
    service_module_category_id: int
    email: EmailStr
    phone_number: str
    created_by: Optional[int]
    created_date: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True


class GeneralEducationRegistrationCreate(BaseModel):
    partner_registration_id: int
    name: str
    registration_type_id: int
    pan_number: str
    upload_fire_safety_certificate: str
    address_pincode: str
    official_email: EmailStr
    gst_registration: Optional[bool] = None
    upload_gst_certificate: Optional[str] = None
    bank_account: Optional[str] = None
    trade_license: Optional[bool] = None
    noc: Optional[bool] = None
    building_type_id: Optional[int] = None
    upload_rental_agreement: Optional[str] = None
    phone_number: Optional[str] = None
    verify_official_email: Optional[str] = None
    created_by: Optional[int] = None

class GeneralEducationRegistrationResponse(BaseModel):
    id: int
    partner_registration_id: int
    name: str
    registration_type_id: int
    pan_number: str
    upload_fire_safety_certificate: str
    address_pincode: str
    official_email: EmailStr
    gst_registration: Optional[bool] = None
    upload_gst_certificate: Optional[str] = None
    bank_account: Optional[str] = None
    trade_license: Optional[bool] = None
    noc: Optional[bool] = None
    building_type_id: Optional[int] = None
    upload_rental_agreement: Optional[str] = None
    phone_number: Optional[str] = None
    verify_official_email: Optional[str] = None
    created_by: Optional[int] = None
    class Config:
        from_attributes = True