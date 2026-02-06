from pydantic import BaseModel,Field
from typing import Optional,List,Dict
from datetime import datetime, time

from decimal import Decimal
import decimal

class IdNameSchema(BaseModel):
    id: int
    name: str


class AppointmentCreateSchema(BaseModel):
    # 🔴 REQUIRED
    user_id: int
    consultation_type_id: int
    appointment_time: datetime

    # 🟡 OPTIONAL
    doctor_id: Optional[int] = None
    doctor_specialization_id: Optional[int] = None

    required_ambulance: Optional[bool] = False
    ambulance_id: Optional[int] = None
    pickup_time: Optional[datetime] = None

    required_assistant: Optional[bool] = False
    assistants_id: Optional[int] = None

    labs_id: Optional[int] = None
    pharmacies_id: Optional[int] = None
    hospital_id: Optional[int] = None

    description: Optional[str] = None
    days_of_suffering: Optional[int] = None
    health_insurance: Optional[bool] = None

    call_booking_status: Optional[str] = "CALL_PENDING"

class AppointmentResponseSchema(BaseModel):
    id: int
    user_id: int
    appointment_time: datetime

    consultation_type_id: Optional[int] = None
    consultation_type_name: Optional[str] = None

    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None

    doctor_specialization_id: Optional[int] = None
    doctor_specialization_name: Optional[str] = None

    ambulance_id: Optional[int] = None
    ambulance_name: Optional[str] = None

    assistants_id: Optional[int] = None
    assistant_name: Optional[str] = None

    labs_id: Optional[int] = None
    lab_name: Optional[str] = None

    pharmacies_id: Optional[int] = None
    pharmacy_name: Optional[str] = None

    hospital_id: Optional[int] = None
    hospital_name: Optional[str] = None

    required_ambulance: Optional[bool]
    required_assistant: Optional[bool]
    pickup_time: Optional[datetime]

    status: Optional[str]
    call_booking_status: Optional[str]
    is_active: bool

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

class HospitalDoctorResponseSchema(BaseModel):
    hospital_id: int
    doctor_id: int
    doctor_name: str

    specialization_id: int
    specialization_name: str

    experience_years: Optional[int] = None
    rating: Optional[float] = None
    fees_per_hour: Optional[float] = None

    available_from: Optional[time] = None
    available_to: Optional[time] = None

    is_available: bool

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


#available_pharmacies:

class AvailablePharmacyCreate(BaseModel):
    
    pharmacy_name: str
    pharmacy_type: Optional[str] = None
    services: Optional[str] = None
    rating: Optional[int] = None
    delivery_time: Optional[str] = None
    latitude: Optional[decimal.Decimal] = None
    longitude: Optional[decimal.Decimal] = None
    upload_prescription: Optional[str] = None
    proceed_type: Optional[str] = None
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None

    open_from: Optional[time] = None
    open_to: Optional[time] = None

    home_delivery: Optional[bool] = False
    created_by: Optional[int] = None



class AvailablePharmacyResponse(BaseModel):
    id: int
    pharmacy_name: str
    pharmacy_type: Optional[str] = None
    services: Optional[str] = None
    rating: Optional[int] = None
    delivery_time: Optional[str] = None
    latitude: Optional[decimal.Decimal] = None
    longitude: Optional[decimal.Decimal] = None
    upload_prescription: Optional[str] = None
    proceed_type: Optional[str] = None
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None

    open_from: Optional[time] = None
    open_to: Optional[time] = None

    home_delivery: Optional[bool] = False
    created_by: Optional[int] = None
    is_active: bool

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





class DoctorAppointmentResponseSchema(BaseModel):
    appointment_id: int
    doctor_name: str
    appointment_time: datetime
    call_booking_status: Optional[str]

    class Config:
        from_attributes = True

class CallBookingStatusUpdateSchema(BaseModel):
    call_booking_status: str


class AppointmentAssignAssistantSchema(BaseModel):
    assistants_id: int
class MasterAssistantResponseSchema(BaseModel):
    id: int
    name: str
    cost_per_visit: decimal.Decimal
    services: List[str] 
    hospital_id:int
    rating:Optional[decimal.Decimal]=None
    role:Optional[str]=None
    is_active:bool
    currency:Optional[str]=None
    class Config:
        from_attributes = True