from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from datetime import time
from decimal import Decimal

#appointment
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


#doctor

class DoctorCreateSchema(BaseModel):
    user_id: int
    specialization_id: int
    experience_years: Optional[int] = None
    rating: Optional[int] = None
    fees_per_hour: Optional[Decimal] = None
    available_from: Optional[time] = None
    available_to: Optional[time] = None
    is_available: Optional[bool] = True

    class Config:
        orm_mode = True


class DoctorResponseSchema(BaseModel):
    id: int
    user_id: int
    specialization_id: int
    experience_years: Optional[int]
    rating: Optional[int]
    fees_per_hour: Optional[Decimal]
    available_from: Optional[time]
    available_to: Optional[time]
    is_available: Optional[bool]

    class Config:
        orm_mode = True

class HospitalAmbulanceResponseSchema(BaseModel):
    hospital_id: int
    hospital_name: str
    ambulance_id: int
    ambulance_number: Optional[str]
    availability_status: Optional[str]
    contact_number: Optional[str]

    class Config:
        orm_mode = True


class AmbulanceBookingCreateSchema(BaseModel):
    user_id: int
    appointment_id: int
    ambulance_id: int
    patient_name: Optional[str] = None
    aadhar_number: Optional[str] = None

    class Config:
        orm_mode = True

class AmbulanceBookingResponseSchema(BaseModel):
    id: int
    appointment_id: int
    ambulance_id: int

    patient_name: Optional[str] = None
    aadhar_number: Optional[str] = None
    is_active: Optional[bool] = None

    # From MasterAmbulance
    service_provider: Optional[str] = None
    contact_number: Optional[str] = None

    class Config:
        orm_mode = True