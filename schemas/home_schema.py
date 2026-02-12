from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
import base64
from pydantic import field_validator


#HomeServiceBookingAddOn
# -------- CREATE --------
class HomeServiceBookingAddOnCreate(BaseModel):
    home_service_booking_id: int
    add_on_id: int
    duration_id: Optional[int] = None
    created_by: Optional[int] = None

# -------- RESPONSE --------
class HomeServiceBookingAddOnResponse(BaseModel):
    id: int
    home_service_booking_id: int
    add_on_id: int
    duration_id: Optional[int]
    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True

class HomeServicePaymentCreate(BaseModel):
    booking_id: int
    user_id: int
    item_total: Decimal
    total_paid: Decimal
    payment_mode: Optional[str] = None
    payment_gateway: Optional[str] = None
    transaction_id: Optional[str] = None
    convenience_fee: Optional[Decimal] = 0
    payment_status: Optional[str] = None
    created_by: Optional[int] = None

#HomeServicePayment
# -------- RESPONSE --------
class HomeServicePaymentResponse(BaseModel):
    id: int
    booking_id: int
    user_id: int
    item_total: Decimal
    total_paid: Decimal
    payment_mode: Optional[str]
    payment_gateway: Optional[str]
    transaction_id: Optional[str]
    convenience_fee: Optional[Decimal]
    payment_status: Optional[str]
    payment_date: Optional[datetime]
    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]
    is_active: Optional[bool]
from typing import Optional, Dict
from decimal import Decimal
from datetime import date, datetime


class HomeServiceBookingCreateSchema(BaseModel):
    module_id: int
    sub_module_id: int
    service_id: int
    sub_service_id: int

    full_name: str
    email: str
    mobile: str
    address: str
    preferred_date: date

    service_summary: Dict
    total_amount: Decimal

    others_address: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None

    time_slot_id: Optional[int] = None
    extra_hours: Optional[int] = 0
    bhk_type_id: Optional[int] = None
    brand_id: Optional[int] = None
    fuel_id: Optional[int] = None
    garage_id: Optional[int] = None
    garage_service_id: Optional[int] = None
    mechanic_id: Optional[int] = None

    special_instructions: Optional[str] = None
    upload_photos: Optional[str] = None  # base64 string

    @field_validator("upload_photos")
    @classmethod
    def validate_base64(cls, value):
        if value is None:
            return value
        try:
            base64.b64decode(value, validate=True)
        except Exception:
            raise ValueError("upload_photos must be a valid base64 string")
        return value

    payment_done: Optional[bool] = False
    status_id: Optional[int] = None

    convenience_fee: Optional[Decimal] = 0
    item_total: Optional[Decimal] = 0

    created_by: Optional[int] = None

    class Config:
        from_attributes = True


class HomeServiceBookingCreateSchema(HomeServiceBookingCreateSchema):
    pass
class HomeServiceBookingResponseSchema(HomeServiceBookingCreateSchema):
    id: int
    is_active: bool





class MasterMechanicCreateSchema(BaseModel):
    garage_id: int
    user_id: int
    mechanic_name: Optional[str] = None
    rating: Optional[Decimal] = None

    class Config:
        from_attributes = True


class MasterMechanicResponseSchema(BaseModel):
    id: int
    garage_id: int
    user_id: int
    mechanic_name: Optional[str]
    rating: Optional[Decimal]
    is_active: bool

    class Config:
        from_attributes = True



class HomeServiceBookingMapCreateSchema(BaseModel):
    home_service_booking_id: int
    garage_service_id: int
    quantity: Optional[int] = 1
    service_price: Optional[Decimal] = None
    created_by: Optional[int] = None


class HomeServiceBookingMapResponseSchema(HomeServiceBookingMapCreateSchema):
    id: int
    created_date: Optional[datetime]
    is_active: Optional[bool]


    class Config:
        from_attributes = True
