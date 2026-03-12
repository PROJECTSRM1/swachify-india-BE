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


class FoodOrderRefundRequestCreate(BaseModel):
    order_id: int
    customer_id: int
    issue_type: Optional[str] = None
    issue_description: Optional[str] = None
    issue_photos: Optional[str] = None
    refund_amount: Optional[Decimal] = None


class FoodOrderRefundRequestResponse(BaseModel):
    id: int
    order_id: int
    customer_id: int
    issue_type: Optional[str]
    issue_description: Optional[str]
    issue_photos: Optional[str]
    refund_status: Optional[str]
    refund_amount: Optional[Decimal]
    created_date: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True


class FoodOrderStatusHistoryCreate(BaseModel):

    order_id: int
    status: Optional[str] = None
    remarks: Optional[str] = None
    created_by: int


class FoodOrderRefundRequestCreate(BaseModel):

    order_id: int
    customer_id: int
    issue_type: Optional[str] = None
    issue_description: Optional[str] = None
    issue_photos: Optional[str] = None
    refund_amount: Optional[Decimal] = None
    created_by: int


class FoodOrderReviewCreate(BaseModel):

    order_id: int
    customer_id: int
    restaurant_id: int
    rating: Optional[Decimal] = None
    review_text: Optional[str] = None
    review_photos: Optional[str] = None
    created_by: int


class MyFoodRegistrationBase(BaseModel):
    partner_registration_id: int
    restaurant_name: str
    restaurant_photo: str
    establishment_year: int
    cuisine_type: dict
    seating_capacity: int
    owner_name: str
    owner_phone_number: str
    business_registration_number: str
    special_menu_items: dict
    average_price_per_meal: Decimal
    operating_hours: str
    upload_menu_card: str
    upload_business_registration_certificate: str
    upload_fssai_license_certificate: str
    upload_gst_certificate: str
    upload_owner_id_proof: str
    upload_owner_address_proof: str
    upload_food_license_certificate: str
    upload_health_inspection_report: str
    upload_fire_noc_certificate: str
    manager_name: Optional[str] = None
    manager_phone_number: Optional[str] = None
    fssai_license_registered: Optional[bool] = None
    fssai_license_number: Optional[str] = None
    gst_registered: Optional[bool] = None
    gst_number: Optional[str] = None
    food_license_applicable: Optional[bool] = None
    food_license_number: Optional[str] = None
    health_safety_certfied: Optional[bool] = None
    health_inspection_certifiate_number: Optional[str] = None
    fire_noc_certficate: Optional[bool] = None
    fire_noc_number: Optional[str] = None
    avialable_dining_options: Optional[dict] = None
    created_by: Optional[int] = None
    modified_by: Optional[int] = None
    is_active: Optional[bool] = True


class MyFoodRegistrationCreate(MyFoodRegistrationBase):
    pass


class MyFoodRegistrationUpdate(MyFoodRegistrationBase):
    pass


class MyFoodRegistrationResponse(MyFoodRegistrationBase):
    id: int
    created_date: Optional[datetime]
    modified_date: Optional[datetime]

    class Config:
        orm_mode = True
