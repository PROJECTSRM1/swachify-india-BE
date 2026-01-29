from pydantic import BaseModel, Field
from typing import Optional


from datetime import date, datetime
from decimal import Decimal

class MasterModuleBase(BaseModel):
    module_name: str = Field(..., min_length=2)
    is_active: bool = True

    model_config = {
        "from_attributes": True 
    }
class MasterModuleCreate(MasterModuleBase):
    pass

class MasterModuleUpdate(BaseModel):
    module_name: Optional[str] = None 
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }
class MasterModuleResponse(MasterModuleBase):
    id: int





# POST REQUEST SCHEMA
class VehicleServiceBookingCreateSchema(BaseModel):
    sub_service_id: int
    brand_id: int
    fuel_id: int
    garage_id: int
    mechanic_id: Optional[int] = None
    problem_description: Optional[str] = None
    address: Optional[str] = None
    customer_name: Optional[str] = None
    contact_number: Optional[str] = None
    preferred_date: Optional[date] = None
    time_slot_id: Optional[int] = None
    image_urls: Optional[str] = None
    items_total: Optional[Decimal] = None
    garage_base_fee: Optional[Decimal] = None
    final_amount: Optional[Decimal] = None
    user_id: Optional[int] = None



# GET RESPONSE SCHEMA
class VehicleServiceBookingResponseSchema(BaseModel):
    id: int
    sub_service_id: int
    brand_id: int
    fuel_id: int
    garage_id: int
    mechanic_id: Optional[int]
    problem_description: Optional[str]
    address: Optional[str]
    customer_name: Optional[str]
    contact_number: Optional[str]
    preferred_date: Optional[date]
    time_slot_id: Optional[int]
    image_urls: Optional[str]
    items_total: Optional[Decimal]
    garage_base_fee: Optional[Decimal]
    final_amount: Optional[Decimal]
    created_date: Optional[datetime]
    is_active: Optional[bool]
    user_id: Optional[int]

    class Config:
        from_attributes = True



class VehicleBrandFuelCreateSchema(BaseModel):
    sub_service_id: int
    brand_id: int
    fuel_id: int


class VehicleBrandFuelResponseSchema(BaseModel):
    id: int
    sub_service_id: int
    brand_id: int
    fuel_id: int
    is_active: Optional[bool]
    created_by: Optional[int]
    created_date: Optional[datetime]

    class Config:
        from_attributes = True
        


class BookingServiceMappingCreateSchema(BaseModel):
    booking_id: int
    garage_service_id: int
    quantity: Optional[int] = None
    service_price: Optional[Decimal] = None


class BookingServiceMappingResponseSchema(BaseModel):
    id: int
    booking_id: int
    garage_service_id: int
    quantity: Optional[int]
    service_price: Optional[Decimal]
    is_active: Optional[bool]
    created_by: Optional[int]
    created_date: Optional[datetime]

    class Config:
        from_attributes = True