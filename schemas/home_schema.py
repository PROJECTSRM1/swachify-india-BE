from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional

# =====================================================
# BASE (matches NON-DB fields used for create)
# =====================================================

class HomeServiceBase(BaseModel):
    module_id: int = Field(..., gt=0)
    sub_module_id: int = Field(..., gt=0)
    service_id: int = Field(..., gt=0)

    full_name: str
    email: EmailStr
    mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")

    address: str

    # Optional in DB
    sub_service_id: Optional[int] = None
    service_type_id: Optional[int] = None
    issue_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None
    preferred_date: Optional[date] = None
    time_slot_id: Optional[int] = None
    special_instructions: Optional[str] = None
    payment_type_id: Optional[int] = None
    service_price: Optional[float] = None
    others_address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    duration_id: Optional[int] = None

    model_config = {"from_attributes": True}


# =====================================================
# CREATE
# =====================================================

class HomeServiceCreate(HomeServiceBase):
    pass


# =====================================================
# UPDATE (PATCH)
# =====================================================

class HomeServiceUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(None, pattern=r"^[6-9]\d{9}$")

    address: Optional[str] = None
    others_address: Optional[str] = None

    sub_service_id: Optional[int] = None
    service_type_id: Optional[int] = None
    issue_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None

    preferred_date: Optional[date] = None
    time_slot_id: Optional[int] = None
    duration_id: Optional[int] = None

    payment_type_id: Optional[int] = None
    service_price: Optional[float] = None
    payment_done: Optional[bool] = None

    assigned_to: Optional[int] = None
    status_id: Optional[int] = None
    work_status_id: Optional[int] = None
    rating: Optional[int] = None
    is_active: Optional[bool] = None


# =====================================================
# RESPONSE (STRICT – matches DB exactly)
# =====================================================

class HomeServiceResponse(BaseModel):
    id: int

    module_id: int
    sub_module_id: int
    service_id: int
    full_name: str
    email: EmailStr
    mobile: str
    address: str

    # Optional in DB
    sub_service_id: Optional[int] = None
    service_type_id: Optional[int] = None
    issue_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None
    preferred_date: Optional[date] = None
    time_slot_id: Optional[int] = None
    special_instructions: Optional[str] = None
    payment_type_id: Optional[int] = None
    service_price: Optional[float] = None
    payment_done: Optional[bool] = None
    assigned_to: Optional[int] = None
    status_id: Optional[int] = None
    rating: Optional[int] = None
    duration_id: Optional[int] = None
    others_address: Optional[str] = None
    work_status_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_by: Optional[int] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    is_active: Optional[bool] = None

    model_config = {"from_attributes": True}


# =====================================================
# CREATE RESPONSE
# =====================================================

class HomeServiceCreateResponse(BaseModel):
    success: bool
    message: str
    service_id: Optional[int] = None


# =====================================================
# RATING UPDATE
# =====================================================

class HomeServiceRatingUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
