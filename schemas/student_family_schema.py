from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

# =============================
# CREATE / UPDATE
# =============================

class StudentFamilyMemberCreate(BaseModel):
    relation_type_id: int = Field(..., gt=0)
    first_name: str
    last_name: Optional[str] = None
    phone_number: Optional[str] = Field(
        None,
        pattern=r"^\d{10}$",
        description="Phone number must be a 10-digit number"
    )


class StudentFamilyMemberUpdate(BaseModel):
    relation_type_id: Optional[int] = Field(None, gt=0)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = Field(
        None,
        pattern=r"^\d{10}$",
        description="Phone number must be a 10-digit number"
    )


# =============================
# RESPONSE
# =============================

class StudentFamilyMemberResponse(BaseModel):
    id: int
    user_id: int

    relation_type_id: int
    relation_type: str        # ← string (Father / Mother / etc)

    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]  # 10-digit phone number

    created_date: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True
