from pydantic import BaseModel, Field ,field_validator
from typing import Optional
from datetime import datetime, time
from decimal import Decimal
import base64

# ======================================================
# PROPERTY SELL LISTING SCHEMAS
# ======================================================

# =========================
# BASE (COMMON FIELDS)
# =========================

# ======================================================
# PROPERTY SELL LISTING SCHEMAS
# ======================================================

import base64
from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal
from datetime import datetime, time


import base64
from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal
from datetime import datetime, time


class PropertySellListingBase(BaseModel):

    module_id: int

    bhk_type_id: Optional[int] = None
    furnishing_id: Optional[int] = None
    locality_area: Optional[str] = None
    upload_photos: Optional[str] = None

    property_type_id: Optional[int] = None
    listing_type_id: Optional[int] = None
    item_condition_id: Optional[int] = None
    hostel_type_id: Optional[int] = None
    land_type_id: Optional[int] = None
    room_type_id: Optional[int] = None
    property_type_facilities_id: Optional[int] = None
    registration_status_id: Optional[int] = None
    star_rating_id: Optional[int] = None

    expected_price: Optional[Decimal] = None
    monthly_rent: Optional[Decimal] = None
    property_sqft: Optional[Decimal] = None
    rating: Optional[Decimal] = None
    registration_value: Optional[Decimal] = None
    distance_km: Optional[Decimal] = None
    price_per_night: Optional[Decimal] = None

    total_rooms: Optional[int] = None
    available_rooms: Optional[int] = None
    rooms_per_floor: Optional[int] = None
    beds_per_room: Optional[int] = None
    sharing_type: Optional[int] = None
    year: Optional[int] = None

    food_included: Optional[bool] = None
    current_bill_excluded: Optional[bool] = None

    location: Optional[int] = None
    owner_name: Optional[str] = None
    mobile_number: Optional[str] = None
    band_name: Optional[str] = None
    model_name: Optional[str] = None
    hotel_name: Optional[str] = None

    upload_document: Optional[str] = None
    property_description: Optional[str] = None

    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None

    user_id: Optional[int] = None
    is_active: Optional[bool] = True


class PropertySellListingCreate(PropertySellListingBase):

    created_by: Optional[int] = None


# @field_validator("upload_photos")
# @classmethod
# def validate_base64(cls, value):
#     if value is None:
#         raise ValueError("upload_photos is required and must be base64")
#
#     try:
#         base64.b64decode(value, validate=True)
#         return value
#     except Exception:
#         raise ValueError("upload_photos must be a valid base64 string")


class PropertySellListingUpdate(PropertySellListingBase):

    modified_by: Optional[int] = None


# @field_validator("upload_photos")
# @classmethod
# def validate_base64(cls, value):
#     if value is None:
#         return value
#
#     try:
#         base64.b64decode(value, validate=True)
#         return value
#     except Exception:
#         raise ValueError("upload_photos must be a valid base64 string")


class PropertySellListingResponse(PropertySellListingBase):

    id: int
    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]

    class Config:
        from_attributes = True


# ======================================================
# PROPERTY LISTING SCHEMAS
# ======================================================

# =========================
# BASE
# =========================

class PropertyListingBase(BaseModel):

    property_sell_listing_id: int
    user_id: int

    full_name: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    is_active: Optional[bool] = True


# =========================
# CREATE
# =========================

class PropertyListingCreate(PropertyListingBase):

    created_by: Optional[int] = None


# =========================
# UPDATE
# =========================

class PropertyListingUpdate(BaseModel):

    full_name: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

    modified_by: Optional[int] = None
    is_active: Optional[bool] = None


# =========================
# RESPONSE
# =========================

class PropertyListingResponse(PropertyListingBase):

    id: int
    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]

    class Config:
        from_attributes = True


# ======================================================
# COMPOSITE RESPONSE
# ======================================================

class PropertyCompositeResponse(BaseModel):

    property_sell_listing: Optional[PropertySellListingResponse] = None
    property_listing: Optional[PropertyListingResponse] = None
    services: Optional["PropertySellListingServicePayload"] = None
    message: str
