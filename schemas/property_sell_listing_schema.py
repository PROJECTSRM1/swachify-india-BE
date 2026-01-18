from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class PropertySellListingCreate(BaseModel):
    # -------- REQUIRED (nullable=False) --------
    module_id: int
    sub_module_id: int
    bhk_type_id: int
    furnishing_id: int
    parking_id: int
    city_id: int
    locality_area: str
    landmark: str
    pincode: int
    upload_photos: str
    owner_name: str
    mobile_number: str

    # -------- OPTIONAL (nullable=True / Optional) --------
    property_type_id: Optional[int] = None
    land_type_id: Optional[int] = None
    plot_area: Optional[Decimal] = None
    length_breadth: Optional[str] = None
    facing_id: Optional[int] = None
    road_width: Optional[Decimal] = None
    boundary_type_id: Optional[int] = None
    water_availability: Optional[bool] = None
    electricity_connection: Optional[bool] = None
    approval_type_id: Optional[int] = None
    ownership_type_id: Optional[int] = None
    expected_price: Optional[Decimal] = None
    negotiable: Optional[bool] = None
    road_access: Optional[str] = None
    suitable_for: Optional[str] = None
    warehouse: Optional[str] = None
    monthly_rent: Optional[Decimal] = None
    lease_duration: Optional[str] = None
    security_deposit: Optional[Decimal] = None
    available_from: Optional[date] = None
    built_up_area: Optional[Decimal] = None
    carpet_area: Optional[Decimal] = None
    floor_number: Optional[int] = None
    total_floors: Optional[int] = None
    property_age: Optional[int] = None
    preferred_tenants_id: Optional[int] = None
    bathrooms: Optional[int] = None
    maintenance_charges: Optional[Decimal] = None
    balconies: Optional[int] = None
    lease_type_id: Optional[int] = None
    availability_status_id: Optional[int] = None
    state_id: Optional[int] = None
    upload_videos: Optional[str] = None
    property_description: Optional[str] = None
    email: Optional[str] = None
    best_time_to_call: Optional[str] = None
    posted_by_id: Optional[int] = None
    created_by: Optional[int] = None

    class Config:
        from_attributes = True



class PropertySellListingResponse(BaseModel):
    # -------- PRIMARY KEY --------
    id: int

    # -------- REQUIRED (from model) --------
    module_id: int
    sub_module_id: int
    bhk_type_id: int
    furnishing_id: int
    parking_id: int
    city_id: int
    locality_area: str
    landmark: str
    pincode: int
    upload_photos: str
    owner_name: str
    mobile_number: str

    # -------- OPTIONAL --------
    property_type_id: Optional[int] = None
    land_type_id: Optional[int] = None
    plot_area: Optional[Decimal] = None
    length_breadth: Optional[str] = None
    facing_id: Optional[int] = None
    road_width: Optional[Decimal] = None
    boundary_type_id: Optional[int] = None
    water_availability: Optional[bool] = None
    electricity_connection: Optional[bool] = None
    approval_type_id: Optional[int] = None
    ownership_type_id: Optional[int] = None
    expected_price: Optional[Decimal] = None
    negotiable: Optional[bool] = None
    road_access: Optional[str] = None
    suitable_for: Optional[str] = None
    warehouse: Optional[str] = None
    monthly_rent: Optional[Decimal] = None
    lease_duration: Optional[str] = None
    security_deposit: Optional[Decimal] = None
    available_from: Optional[date] = None
    built_up_area: Optional[Decimal] = None
    carpet_area: Optional[Decimal] = None
    floor_number: Optional[int] = None
    total_floors: Optional[int] = None
    property_age: Optional[int] = None
    preferred_tenants_id: Optional[int] = None
    bathrooms: Optional[int] = None
    maintenance_charges: Optional[Decimal] = None
    balconies: Optional[int] = None
    lease_type_id: Optional[int] = None
    availability_status_id: Optional[int] = None
    state_id: Optional[int] = None
    upload_videos: Optional[str] = None
    property_description: Optional[str] = None
    email: Optional[str] = None
    best_time_to_call: Optional[str] = None
    posted_by_id: Optional[int] = None
    created_by: Optional[int] = None

    # -------- SYSTEM FIELDS --------
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class PropertyListingCreate(BaseModel):
    property_sell_listing_id: int
    user_id: int
    created_by: Optional[int] = None

    class Config:
        from_attributes = True

class PropertyListingResponse(BaseModel):
    id: int

    property_sell_listing_id: int
    user_id: int
    created_by: Optional[int] = None

    created_date: Optional[datetime] = None
    modified_by: Optional[int] = None
    modified_date: Optional[datetime] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True
