

# from pydantic import BaseModel, EmailStr, Field
# from typing import Optional
# from datetime import date


# class HomeServiceBase(BaseModel):
#     module_id: int
#     sub_module_id: int
#     service_id: int
#     sub_service_id: int
#     sub_group_id: int

#     full_name: str = Field(..., min_length=3, max_length=100)
#     email: EmailStr
#     mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")
#     address: str

#     service_type_id: int
#     issue_id: Optional[int] = None
#     problem_description: Optional[str] = None
#     property_size_sqft: Optional[int] = Field(None, gt=0)
#     duration_id: int

#     preferred_date: date
#     time_slot_id: int

#     special_instructions: Optional[str] = None
#     payment_type_id: int
#     service_price: Optional[float] = None

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
#     issue_id: Optional[int] = None
#     problem_description: Optional[str] = None
#     property_size_sqft: Optional[int] = None
#     duration_id: Optional[int] = None

#     preferred_date: Optional[date] = None
#     time_slot_id: Optional[int] = None
#     special_instructions: Optional[str] = None

#     payment_type_id: Optional[int] = None
#     service_price: Optional[float] = None
#     payment_done: Optional[bool] = None

#     assigned_to: Optional[int] = None
#     status_id: Optional[int] = None
#     is_active: Optional[bool] = None

# class HomeServiceResponse(BaseModel):
#     id: int

#     module_id: Optional[int] = None
#     sub_module_id: Optional[int] = None
#     service_id: Optional[int] = None
#     sub_service_id: Optional[int] = None
#     sub_group_id: Optional[int] = None

#     full_name: Optional[str] = None
#     email: Optional[str] = None
#     mobile: Optional[str] = None
#     address: Optional[str] = None

#     service_type_id: Optional[int] = None
#     issue_id: Optional[int] = None
#     problem_description: Optional[str] = None
#     property_size_sqft: Optional[int] = None
#     duration_id: Optional[int] = None

#     preferred_date: Optional[date] = None
#     time_slot_id: Optional[int] = None

#     special_instructions: Optional[str] = None
#     payment_type_id: Optional[int] = None
#     service_price: Optional[float] = None

#     payment_done: bool
#     created_by: int
#     assigned_to: Optional[int] = None
#     status_id: int
#     is_active: bool

#     class Config:
#         from_attributes = True

# class HomeServiceCreateResponse(BaseModel):
#     message: str
#     service_id: int
#     status_id: int
#     status_name: str



from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional


# ==================================================
# 🔹 BASE SCHEMA (Shared Fields)
# ==================================================
class HomeServiceBase(BaseModel):
    module_id: int
    sub_module_id: int
    service_id: int
    sub_service_id: int
    sub_group_id: int

    full_name: str
    email: EmailStr
    mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")
    address: str

    service_type_id: int
    issue_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None
    duration_id: int

    preferred_date: date
    time_slot_id: int

    payment_type_id: int
    service_price: Optional[float] = None
    payment_done: bool = False

    # ✅ INTERNAL FIELD (SET BY BACKEND, NOT CLIENT)
    created_by: Optional[int] = None

    model_config = {"from_attributes": True}


# ==================================================
# 🔹 CREATE SCHEMA (POST)
# ==================================================
class HomeServiceCreate(HomeServiceBase):
    """
    Used for POST /home-service
    created_by is NOT required from client
    """
    pass


# ==================================================
# 🔹 UPDATE SCHEMA (PUT / PATCH)
# ==================================================
class HomeServiceUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(None, pattern=r"^[6-9]\d{9}$")
    address: Optional[str] = None

    issue_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None
    duration_id: Optional[int] = None

    preferred_date: Optional[date] = None
    time_slot_id: Optional[int] = None

    payment_type_id: Optional[int] = None
    service_price: Optional[float] = None
    payment_done: Optional[bool] = None

    assigned_to: Optional[int] = None
    status_id: Optional[int] = None
    is_active: Optional[bool] = None


# ==================================================
# 🔹 RESPONSE SCHEMA (GET / POST RESPONSE)
# ==================================================
class HomeServiceResponse(BaseModel):
    id: int

    module_id: Optional[int] = None
    sub_module_id: Optional[int] = None
    service_id: Optional[int] = None
    sub_service_id: Optional[int] = None
    sub_group_id: Optional[int] = None

    full_name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None      # ✅ NO REGEX IN RESPONSE
    address: Optional[str] = None

    service_type_id: Optional[int] = None
    issue_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None

    duration_id: Optional[int] = None  # ✅ FIXED VALIDATION ERROR

    preferred_date: Optional[date] = None
    time_slot_id: Optional[int] = None

    payment_type_id: Optional[int] = None
    service_price: Optional[float] = None
    payment_done: bool

    created_by: int                    # ✅ VISIBLE
    assigned_to: Optional[int] = None
    status_id: int
    is_active: bool

    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================================================
# 🔹 SIMPLE CREATE RESPONSE (OPTIONAL)
# ==================================================
class HomeServiceCreateResponse(BaseModel):
    message: str
    service_id: int
    status_id: int
    created_by: int

