from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


# ============================
# CREATE (POST) SCHEMA
# ============================
class RawMaterialCreate(BaseModel):
    module_id: int
    raw_material_type_id: int
    quantity: int = Field(gt=0)
    cost: Decimal = Field(gt=0)
    latitude: Decimal
    longitude: Decimal


# ============================
# RESPONSE (GET) SCHEMA
# ============================
class RawMaterialResponse(BaseModel):
    id: int
    module_id: int
    raw_material_type_id: int
    quantity: int
    cost: Decimal
    latitude: Decimal
    longitude: Decimal
    is_active: Optional[bool]
    created_date: Optional[datetime]

    class Config:
        from_attributes = True   # IMPORTANT for SQLAlchemy
