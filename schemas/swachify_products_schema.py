from pydantic import BaseModel
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
    is_active: Optional[bool] = True


# ======================
# CREATE
# ======================

class ProductRegistrationCreate(ProductRegistrationBase):
    created_by: Optional[int] = None


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
