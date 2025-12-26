# from pydantic import BaseModel, EmailStr
# from datetime import date
# from typing import Optional


# # 🔹 Base schema (shared fields)
# class HomeServiceBase(BaseModel):
#     module_id: int
#     sub_module_id: int
#     service_id: int
#     sub_service_id: int
#     sub_group_id: int

#     full_name: str
#     email: EmailStr
#     mobile: str
#     address: str

#     service_type_id: int
#     problem_description: Optional[str] = None
#     property_size_sqft: Optional[int] = None

#     preferred_date: date
#     time_slot_id: int
#     special_instructions: Optional[str] = None

#     payment_type_id: int
#     service_price: Optional[float] = None

#     model_config = {
#         "from_attributes": True
#     }


# # 🔹 CREATE (frontend → backend)
# class HomeServiceCreate(HomeServiceBase):
#     payment_done: bool 
#     created_by: int  


# # 🔹 UPDATE (partial update allowed)
# class HomeServiceUpdate(BaseModel):
#     module_id: Optional[int] = None
#     sub_module_id: Optional[int] = None
#     service_id: Optional[int] = None
#     sub_service_id: Optional[int] = None
#     sub_group_id: Optional[int] = None

#     full_name: Optional[str] = None
#     email: Optional[EmailStr] = None
#     mobile: Optional[str] = None
#     address: Optional[str] = None

#     service_type_id: Optional[int] = None
#     problem_description: Optional[str] = None
#     property_size_sqft: Optional[int] = None

#     preferred_date: Optional[date] = None
#     time_slot_id: Optional[int] = None
#     special_instructions: Optional[str] = None

#     payment_type_id: Optional[int] = None
#     service_price: Optional[float] = None
#     payment_done: Optional[bool] = None


# # class HomeServiceResponse(HomeServiceBase):
# #     id: int
# #     payment_done: bool
# #     created_by: int


# class HomeServiceResponse(HomeServiceBase):
#     id: int
#     payment_done: Optional[bool] = None
#     created_by: Optional[int] = None



from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# 🔹 BASE SCHEMA (shared fields)
class HomeServiceBase(BaseModel):
    # Service hierarchy
    module_id: int
    sub_module_id: int
    service_id: int
    sub_service_id: int
    sub_group_id: int

    # Customer details
    full_name: str
    email: EmailStr
    mobile: str
    address: str

    # Service details
    service_type_id: int
    problem_description: Optional[str] = None
    property_size_sqft: Optional[int] = None

    # Scheduling
    preferred_date: date
    time_slot_id: int
    special_instructions: Optional[str] = None

    # Payment
    payment_type_id: int
    service_price: Optional[float] = None

    model_config = {
        "from_attributes": True
    }


# 🔹 CREATE SCHEMA (frontend → backend)
class HomeServiceCreate(HomeServiceBase):
    payment_done: bool = False

    # ✅ System fields (explicitly included as requested)
    created_by: int                  # user_id
    assigned_to: Optional[int] = None  # freelancer_id
    status_id: int                   # FK → master_status.id


# 🔹 UPDATE SCHEMA
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

    # System-controlled updates
    assigned_to: Optional[int] = None
    status_id: Optional[int] = None


# 🔹 RESPONSE SCHEMA (backend → frontend)
class HomeServiceResponse(HomeServiceBase):
    id: int
    payment_done: bool
    created_by: int
    assigned_to: Optional[int] = None
    status_id: int

class HomeServiceFilter(BaseModel):
    created_by: int
    payment_done: Optional[bool] = None

class AssignFreelancerRequest(BaseModel):
    home_service_id: int
    freelancer_id: int