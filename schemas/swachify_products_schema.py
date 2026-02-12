from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

# ======================
# BASE SCHEMA
# ======================

class ProductRegistrationBase(BaseModel):
    user_id: int
    category_id: int
    company_name: Optional[str] = None
    product_name: Optional[str] = None
    address: Optional[str] = None
    product_price: Optional[Decimal] = None
    description: Optional[str] = None
    product_image: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = True


# ======================
# CREATE
# ======================

class ProductRegistrationCreate(ProductRegistrationBase):
      pass

# ======================
# UPDATE
# ======================

class ProductRegistrationUpdate(ProductRegistrationBase):
    modified_by: Optional[int] = None


# ======================
# RESPONSE
# ======================

class ProductRegistrationResponse(ProductRegistrationBase):
    id: int
    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]

    class Config:
        from_attributes = True


# ===============================
# CREATE ORDER
# ===============================

class ProductOrderCreate(BaseModel):
    user_id: int
    product_id: int
    full_name: str = Field(..., max_length=255)
    phone_number: str = Field(..., max_length=20)
    delivery_address: str
    quantity: str
    vehicle_type_id: Optional[int] = None
    created_by: Optional[int] = None


# ===============================
# RESPONSE SCHEMA
# ===============================

class ProductOrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    full_name: str
    phone_number: str
    delivery_address: str
    quantity: str
    vehicle_type_id: Optional[int]
    order_date: Optional[datetime]
    status: Optional[str]
    is_active: Optional[bool]

    class Config:
        from_attributes = True