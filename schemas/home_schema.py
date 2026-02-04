from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import date, datetime
from decimal import Decimal


class HomeServiceBookingCreate(BaseModel):
    module_id: int
    sub_module_id: int
    service_id: int
    sub_service_id: int
    full_name: str
    email: EmailStr
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
    fule_id: Optional[int] = None   # ✅ MATCH MODEL
    garage_id: Optional[int] = None
    garage_service_id: Optional[int] = None
    mechanic_id: Optional[int] = None
    special_instructions: Optional[str] = None
    upload_photos: Optional[str] = None
    payment_done: Optional[bool] = False
    status_id: Optional[int] = None
    created_by: Optional[int] = None
    convenience_fee: Optional[Decimal] = Decimal("0.00")
    home_service_payment_id: Optional[int] = None
    item_total: Optional[Decimal] = Decimal("0.00")

    class Config:
        from_attributes = True





class HomeServiceBookingResponse(BaseModel):
    id: int

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
    convenience_fee: Optional[Decimal]
    item_total: Optional[Decimal]

    others_address: Optional[str]
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    time_slot_id: Optional[int]
    extra_hours: Optional[int]

    bhk_type_id: Optional[int]
    brand_id: Optional[int]
    fule_id: Optional[int]          # ✅ MATCHES MODEL
    garage_id: Optional[int]
    garage_service_id: Optional[int]
    mechanic_id: Optional[int]

    special_instructions: Optional[str]
    upload_photos: Optional[str]

    payment_done: Optional[bool]
    status_id: Optional[int]

    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]

    is_active: Optional[bool]

    home_service_payment_id: Optional[int]

    class Config:
        from_attributes = True   # ✅ Pydantic v2 compatible