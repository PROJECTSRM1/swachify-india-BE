from pydantic import BaseModel
from typing import Optional


class StudentInternshipStatusCreate(BaseModel):
    internship_status: str


class StudentInternshipStatusResponse(BaseModel):
    user_id: int
    internship_status: Optional[str]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
