from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentCreateSchema(BaseModel):
    user_id: int
    consultation_type: str
    appointment_time: datetime

    doctor_id: Optional[int] = None
    doctor_specialization_id: Optional[int] = None
    description: Optional[str] = None
    days_of_suffering: Optional[int] = None

    required_ambulance: Optional[bool] = False
    ambulance_id: Optional[int] = None
    pickup_time: Optional[datetime] = None

    class Config:
        orm_mode = True

class AppointmentResponseSchema(BaseModel):
    id: int
    user_id: int
    consultation_type: str
    appointment_time: datetime
    required_ambulance: Optional[bool]
    ambulance_id: Optional[int]

    class Config:
        orm_mode = True
