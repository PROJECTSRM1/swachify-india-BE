from pydantic import BaseModel,Field
from typing import Optional, List
from datetime import datetime, time

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

class IdNameSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
class AppointmentResponseSchema(BaseModel):
    id: int
    user_id: int
    appointment_time: datetime

    # ---------- IDs (existing) ----------
    consultation_type_id: Optional[int] = None
    consultation_type: Optional[IdNameSchema] = None
    doctor_id: Optional[int] = None
    doctor: Optional[IdNameSchema] = None
    doctor_specialization_id: Optional[int] = None
    doctor_specialization: Optional[IdNameSchema] = None
    ambulance_id: Optional[int] = None
    ambulance: Optional[IdNameSchema] = None
    assistant_id: Optional[int] = None
    assistant: Optional[IdNameSchema] = None

    labs_id: Optional[int] = None
    labs: Optional[IdNameSchema] = None

    pharmacies_id: Optional[int] = None
    pharmacies: Optional[IdNameSchema] = None

    # ---------- Names (NEW) ----------
    hospital: Optional[IdNameSchema] = None

    # ---------- Other fields ----------
    required_ambulance: Optional[bool] = None
    required_assistant: Optional[bool] = None
    pickup_time: Optional[datetime] = None
    status: Optional[str] = None
    is_active: bool
    call_booking_status: Optional[str] = None


    class Config:
        from_attributes = True

#doctor
class DoctorCreateSchema(BaseModel):
    user_id: int
    specialization_id: int

    experience_years: Optional[int] = Field(None, ge=0)
    rating: Optional[Decimal] = Field(
        None,
        ge=Decimal("1.0"),
        le=Decimal("5.0")
    )
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
    rating: Optional[Decimal] 
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


class PaymentCreateSchema(BaseModel):
    service_request_id: int
    user_id: int
    amount: Decimal = Field(..., gt=0)
    payment_method: str  # CARD | UPI | CASH
    appointment_id: Optional[int] = None
    transaction_id: Optional[str] = None
    remarks: Optional[str] = None

    class Config:
        from_attributes = True


class PaymentResponseSchema(BaseModel):
    id: int
    service_request_id: int
    user_id: int
    amount: Decimal
    payment_method: str
    appointment_id: Optional[int]
    payment_status: Optional[str]
    transaction_id: Optional[str]
    remarks: Optional[str]
    created_date: datetime

    class Config:
        from_attributes = True
        
        
        


# -------- CREATE SCHEMA (POST) --------
class AvailableLabCreate(BaseModel):
    lab_name: str
    services: Optional[str] = None
    rating: Optional[int] = None
    home_collection: Optional[bool] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    upload_prescription: Optional[str] = None
    proceed_type: Optional[str] = None
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None
    specialization_id: Optional[int] = None
    fees_per_test: Optional[Decimal] = None
    available_from: Optional[time] = None
    available_to: Optional[time] = None
    estimated_delivery: Optional[str] = None


# -------- RESPONSE SCHEMA (GET) --------
class AvailableLabResponse(BaseModel):
    id: int
    lab_name: str
    services: Optional[str]
    rating: Optional[int]
    home_collection: Optional[bool]
    is_active: Optional[bool]
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    specialization_id: Optional[int]
    fees_per_test: Optional[Decimal]
    available_from: Optional[time]
    available_to: Optional[time]
    estimated_delivery: Optional[str]
    is_available: Optional[bool]

    class Config:
       from_attributes = True
        