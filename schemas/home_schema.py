from pydantic import BaseModel
from typing import Optional, Dict
from decimal import Decimal
from datetime import date



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
    upload_photos: Optional[str] = None


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