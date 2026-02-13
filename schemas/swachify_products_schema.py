from pydantic import BaseModel,Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

# ======================
# BASE SCHEMA
# ======================

class ProductRegistrationBase(BaseModel):
    user_id: int
    category_id: int
    company_name: Optional[str] = None
    product_name: Optional[str] = None
    address: Optional[str] = None
    product_price: Optional[Decimal] = None
    description: Optional[str] = None
    product_image: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = True


# ======================
# CREATE
# ======================

class ProductRegistrationCreate(ProductRegistrationBase):
      pass

# ======================
# UPDATE
# ======================

class ProductRegistrationUpdate(ProductRegistrationBase):
    modified_by: Optional[int] = None


# ======================
# RESPONSE
# ======================

class ProductRegistrationResponse(ProductRegistrationBase):
    id: int
    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]

    class Config:
        from_attributes = True

# =====================================================
# TASK SCHEMAS
# =====================================================

class TaskCreate(BaseModel):
    title: str
    description: str

    task_type_id: int = Field(..., description="Master task type ID")
    project_id: int = Field(..., description="Master project ID")

    # Student / Assignee
    user_id: int = Field(..., description="Student user ID")

    reporting_manager_id: Optional[int] = None
    task_manager_id: Optional[int] = None

    status_id: int = Field(..., description="Master status ID")

    due_date: date
    efforts_in_days: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str

    task_type_id: int
    project_id: int

    user_id: int  # assignee
    reporting_manager_id: Optional[int]
    task_manager_id: Optional[int]

    status_id: int
    due_date: date
    efforts_in_days: Optional[int]

    created_by: int
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class TaskStatusUpdate(BaseModel):
    status_id: int = Field(..., description="New status ID")
    

# ===============================
# CREATE ORDER
# ===============================

class ProductOrderCreate(BaseModel):
    user_id: int
    product_id: int
    full_name: str = Field(..., max_length=255)
    phone_number: str = Field(..., max_length=20)
    delivery_address: str
    quantity: str
    vehicle_type_id: Optional[int] = None
    created_by: Optional[int] = None


# ===============================
# RESPONSE SCHEMA
# ===============================

class ProductOrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    full_name: str
    phone_number: str
    delivery_address: str
    quantity: str
    vehicle_type_id: Optional[int]
    order_date: Optional[datetime]
    status: Optional[str]
    is_active: Optional[bool]

    class Config:
        from_attributes = True


# ===============================
# CREATE
# ===============================

class TaskHistoryCreate(BaseModel):
    task_id: int
    user_id: int
    from_assignee_id: Optional[int] = None
    to_assignee_id: Optional[int] = None
    reporting_manager_id: Optional[int] = None
    comments: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    created_by: Optional[int] = None


# ===============================
# RESPONSE
# ===============================

class TaskHistoryResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    from_assignee_id: Optional[int]
    to_assignee_id: Optional[int]
    reporting_manager_id: Optional[int]
    comments: Optional[str]
    rating: Optional[int]
    created_date: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
