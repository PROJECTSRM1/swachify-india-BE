# schemas/home_service_schema.py
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

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
    add_on_id: Optional[int] = None

    preferred_date: date
    time_slot_id: int
    special_instructions: Optional[str] = None
    payment_type_id: int

    model_config = {
        "from_attributes": True
    }


class HomeServiceCreate(HomeServiceBase):
    pass


class HomeServiceUpdate(HomeServiceCreate):
    pass


class HomeServiceResponse(HomeServiceBase):
    id: int


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
