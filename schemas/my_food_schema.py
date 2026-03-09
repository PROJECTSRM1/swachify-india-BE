from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class FoodOrderCreate(BaseModel):

    customer_id: int
    restaurant_id: int
    location_type: Optional[str]
    location_details: Optional[str]
    customer_name: Optional[str]
    contact_number: Optional[str]
    allocation_type: Optional[str]
    delivery_date: Optional[date]
    delivery_time_slot: Optional[str]
    extra_hours: Optional[int] = 0
    convenience_fee: Optional[Decimal]
    total_amount: Optional[Decimal]


class FoodOrderResponse(BaseModel):

    id: int
    customer_id: int
    restaurant_id: int
    order_date: Optional[datetime]
    location_type: Optional[str]
    location_details: Optional[str]
    customer_name: Optional[str]
    contact_number: Optional[str]
    allocation_type: Optional[str]
    delivery_date: Optional[date]
    delivery_time_slot: Optional[str]
    extra_hours: Optional[int]
    convenience_fee: Optional[Decimal]
    total_amount: Optional[Decimal]
    status: Optional[str]

    class Config:
        from_attributes = True