# 


# from pydantic import BaseModel, EmailStr
# from datetime import date
# from typing import Optional

# class HomeServiceCreate(BaseModel):
#     # ONLY this comes from frontend selection
#     sub_group_id: int

#     # User entered fields
#     full_name: str
#     email: EmailStr
#     mobile: str
#     address: str

#     service_type_id: int
#     problem_description: Optional[str] = None
#     property_size_sqft: Optional[int] = None
#     add_on_id: Optional[int] = None

#     preferred_date: date
#     time_slot_id: int
#     special_instructions: Optional[str] = None
#     payment_type_id: int




from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# 🔹 Base schema (shared fields)
class HomeServiceBase(BaseModel):
    module_id: int
    sub_module_id: int
    service_id: int
    sub_service_id: int
    sub_group_id: int

    full_name: str
    email: EmailStr
    mobile: str
    address: str

    service_type_id: int
    problem_description: Optional[str] = None
    property_size_sqft: Optional[int] = None

    preferred_date: date
    time_slot_id: int
    special_instructions: Optional[str] = None

    payment_type_id: int
    service_price: float

    model_config = {
        "from_attributes": True
    }


# 🔹 CREATE (frontend → backend)
class HomeServiceCreate(HomeServiceBase):
    payment_done: bool  # ✅ REQUIRED while creating service


# 🔹 UPDATE (partial update allowed)
class HomeServiceUpdate(BaseModel):
    module_id: Optional[int] = None
    sub_module_id: Optional[int] = None
    service_id: Optional[int] = None
    sub_service_id: Optional[int] = None
    sub_group_id: Optional[int] = None

    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    address: Optional[str] = None

    service_type_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[int] = None

    preferred_date: Optional[date] = None
    time_slot_id: Optional[int] = None
    special_instructions: Optional[str] = None

    payment_type_id: Optional[int] = None
    service_price: Optional[float] = None
    payment_done: Optional[bool] = None


class HomeServiceResponse(HomeServiceBase):
    id: int
    payment_done: bool
    created_by: int
