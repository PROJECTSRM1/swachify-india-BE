from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional

# =====================================================
# BASE
# =====================================================

class HomeServiceBase(BaseModel):
    module_id: int = Field(..., gt=0)
    sub_module_id: int = Field(..., gt=0)
    service_id: int = Field(..., gt=0)
    sub_service_id: int = Field(..., gt=0)

    full_name: str
    email: EmailStr
    mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")

    address: str
    others_address: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    service_type_id: int = Field(..., gt=0)
    issue_id: Optional[int] = None

    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None

    duration_id: int = Field(..., gt=0)

    preferred_date: date
    time_slot_id: int = Field(..., gt=0)

    payment_type_id: int = Field(..., gt=0)
    service_price: Optional[float] = None
    payment_done: bool = False

    model_config = {"from_attributes": True}


# =====================================================
# CREATE
# =====================================================

class HomeServiceCreate(HomeServiceBase):
    """
    Used for booking a new home service
    """
    pass


# =====================================================
# UPDATE
# =====================================================

class HomeServiceUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(None, pattern=r"^[6-9]\d{9}$")

    address: Optional[str] = None
    others_address: Optional[str] = None

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
    work_status_id: Optional[int] = None
    is_active: Optional[bool] = None


# =====================================================
# DB RESPONSE (INTERNAL USE / GET APIs)
# =====================================================

class HomeServiceResponse(BaseModel):
    id: int

    module_id: int
    sub_module_id: int
    service_id: int
    sub_service_id: int

    full_name: str
    email: str
    mobile: str

    address: str
    others_address: Optional[str] = None

    service_type_id: int
    issue_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None

    duration_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    preferred_date: date
    time_slot_id: int

    payment_type_id: int
    service_price: Optional[float] = None
    payment_done: bool

    created_by: int
    assigned_to: Optional[int] = None

    status_id: int
    work_status_id: int
    is_active: bool

    created_date: datetime
    modified_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# =====================================================
# CREATE RESPONSE (SAFE API RESPONSE)
# =====================================================

# schemas/home_schema.py

class HomeServiceCreateResponse(BaseModel):
    success: bool
    message: str
    service_id: Optional[int] = None
    status_id: Optional[int] = None
    work_status_id: Optional[int] = None
    created_by: Optional[int] = None


# =====================================================
# RATING UPDATE
# =====================================================

class HomeServiceRatingUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
