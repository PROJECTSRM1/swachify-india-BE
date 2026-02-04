from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

#HomeServiceBookingAddOn
# -------- CREATE --------
class HomeServiceBookingAddOnCreate(BaseModel):
    home_service_booking_id: int
    add_on_id: int
    duration_id: Optional[int] = None
    created_by: Optional[int] = None

# -------- RESPONSE --------
class HomeServiceBookingAddOnResponse(BaseModel):
    id: int
    home_service_booking_id: int
    add_on_id: int
    duration_id: Optional[int]
    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True

class HomeServicePaymentCreate(BaseModel):
    booking_id: int
    user_id: int
    item_total: Decimal
    total_paid: Decimal
    payment_mode: Optional[str] = None
    payment_gateway: Optional[str] = None
    transaction_id: Optional[str] = None
    convenience_fee: Optional[Decimal] = 0
    payment_status: Optional[str] = None
    created_by: Optional[int] = None

#HomeServicePayment
# -------- RESPONSE --------
class HomeServicePaymentResponse(BaseModel):
    id: int
    booking_id: int
    user_id: int
    item_total: Decimal
    total_paid: Decimal
    payment_mode: Optional[str]
    payment_gateway: Optional[str]
    transaction_id: Optional[str]
    convenience_fee: Optional[Decimal]
    payment_status: Optional[str]
    payment_date: Optional[datetime]
    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True