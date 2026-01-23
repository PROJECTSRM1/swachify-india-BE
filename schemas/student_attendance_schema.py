from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class StudentAttendanceCreate(BaseModel):
    attendance_percentage: Decimal


class StudentAttendanceResponse(BaseModel):
    user_id: int
    attendance_percentage: Optional[Decimal]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
