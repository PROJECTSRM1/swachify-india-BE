from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

from datetime import time
from decimal import Decimal

class AppointmentCreateSchema(BaseModel):
    user_id: int
    consultation_type_id: int
    appointment_time: datetime

    doctor_id: Optional[int] = None
    doctor_specialization_id: Optional[int] = None
    description: Optional[str] = None
    days_of_suffering: Optional[int] = None

    health_insurance: Optional[bool] = None

    required_ambulance: Optional[bool] = False
    ambulance_id: Optional[int] = None
    pickup_time: Optional[datetime] = None

    required_assistant: Optional[bool] = False
    assistant_id: Optional[int] = None

    labs_id: Optional[int] = None
    pharmacies_id: Optional[int] = None

    class Config:
        from_attributes = True
class AppointmentResponseSchema(BaseModel):
    id: int
    user_id: int
    consultation_type_id: int
    appointment_time: datetime

    doctor_id: Optional[int]
    doctor_specialization_id: Optional[int]

    required_ambulance: Optional[bool]
    ambulance_id: Optional[int]
    pickup_time: Optional[datetime]

    required_assistant: Optional[bool]
    assistant_id: Optional[int]

    labs_id: Optional[int]
    pharmacies_id: Optional[int]

    is_active: bool

    class Config:
        from_attributes = True

#doctor
class DoctorCreateSchema(BaseModel):
    user_id: int
    specialization_id: int

    experience_years: Optional[int] = Field(None, ge=0)
    rating: Optional[int] = Field(None, ge=1, le=5)
    fees_per_hour: Optional[Decimal] = None

    available_from: Optional[time] = None
    available_to: Optional[time] = None
    is_available: Optional[bool] = True

    hospital_id: Optional[int] = None
    consultation_type_id: Optional[int] = None

    class Config:
        from_attributes = True

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

    hospital_id: Optional[int]
    consultation_type_id: Optional[int]

    is_active: bool

    class Config:
        from_attributes = True

class HospitalAmbulanceResponseSchema(BaseModel):
    hospital_id: int
    hospital_name: str
    ambulance_id: int
    ambulance_number: Optional[str]
    availability_status: Optional[str]
    contact_number: Optional[str]

    class Config:
        from_attributes = True


class AmbulanceBookingCreateSchema(BaseModel):
    user_id: int
    appointment_id: int
    ambulance_id: int
    patient_name: Optional[str] = None
    aadhar_number: Optional[str] = None

    class Config:
        from_attributes = True

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
        from_attributes = True
 