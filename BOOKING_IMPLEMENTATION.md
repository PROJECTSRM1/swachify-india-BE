# Booking Services - Complete Implementation Guide

## Overview
This document contains the complete implementation for booking/home services with Razorpay payment integration.

---

## 1. SCHEMA - `schemas/home_schema.py`

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional


# ==================================================
# 🔹 BASE SCHEMA (Shared Fields)
# ==================================================
class HomeServiceBookingBase(BaseModel):
    module_id: int
    sub_module_id: int
    service_id: int
    sub_service_id: int
    sub_group_id: int

    full_name: str
    email: EmailStr
    mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")
    address: str

    service_type_id: int
    issue_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None
    duration_id: int

    preferred_date: date
    time_slot_id: int

    payment_type_id: int
    service_price: Optional[float] = None
    payment_done: bool = False

    # ✅ INTERNAL FIELD (SET BY BACKEND, NOT CLIENT)
    created_by: Optional[int] = None

    model_config = {"from_attributes": True}


# ==================================================
# 🔹 CREATE SCHEMA (POST)
# ==================================================
class HomeServiceBookingBookingCreate(HomeServiceBase):
    """
    Used for POST /api/master/home-service
    created_by is NOT required from client - it's set automatically
    """
    pass


# ==================================================
# 🔹 UPDATE SCHEMA (PUT / PATCH)
# ==================================================
class HomeServiceBookingUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(None, pattern=r"^[6-9]\d{9}$")
    address: Optional[str] = None

    issue_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None
    duration_id: Optional[int] = None

    preferred_date: Optional[date] = None
    time_slot_id: Optional[int] = None

    payment_type_id: Optional[int] = None
    service_price: Optional[float] = None
    payment_done: Optional[bool] = None

    assigned_to: Optional[int] = None
    status_id: Optional[int] = None
    is_active: Optional[bool] = None


# ==================================================
# 🔹 RESPONSE SCHEMA (GET / POST RESPONSE)
# ==================================================
class HomeServiceResponse(BaseModel):
    id: int

    module_id: Optional[int] = None
    sub_module_id: Optional[int] = None
    service_id: Optional[int] = None
    sub_service_id: Optional[int] = None
    sub_group_id: Optional[int] = None

    full_name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None      # ✅ NO REGEX IN RESPONSE
    address: Optional[str] = None

    service_type_id: Optional[int] = None
    issue_id: Optional[int] = None
    problem_description: Optional[str] = None
    property_size_sqft: Optional[str] = None

    duration_id: Optional[int] = None

    preferred_date: Optional[date] = None
    time_slot_id: Optional[int] = None

    payment_type_id: Optional[int] = None
    service_price: Optional[float] = None
    payment_done: bool

    created_by: int                    # ✅ VISIBLE
    assigned_to: Optional[int] = None
    status_id: int
    is_active: bool

    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================================================
# 🔹 CREATE RESPONSE (OPTIONAL)
# ==================================================
class HomeServiceCreateResponse(BaseModel):
    message: str
    service_id: int
    status_id: int
    created_by: int
```

---

## 2. SERVICE - `services/home_service.py`

```python
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.home_service import HomeService
from schemas.home_schema import HomeServiceBase, HomeServiceCreate, HomeServiceUpdate


def create_home_service(db: Session, data: HomeServiceCreate, user_id: int):
    """
    Create a new home service booking.
    
    Args:
        db: Database session
        data: HomeServiceCreate schema containing all service details
        user_id: The user ID (customer) creating the booking
    
    Returns:
        HomeService object with all details
    """
    service = HomeService(
        **data.model_dump(exclude={"created_by"}),
        created_by=user_id,
        status_id=1,
        is_active=True
    )

    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_home_services(db: Session):
    """Get all active home services."""
    return db.query(HomeService).filter(HomeService.is_active == True).all()


def get_home_service(db: Session, service_id: int):
    """Get a specific home service by ID."""
    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")
    return obj


def update_home_service(db: Session, service_id: int, data: HomeServiceUpdate):
    """Update a home service booking."""
    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_home_service(db: Session, service_id: int):
    """Soft delete a home service (mark as inactive)."""
    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")

    obj.is_active = False
    db.commit()
    return {"message": "Service deactivated"}
```

---

## 3. ROUTES - `routes/master_module_route.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_user
from models.master_module import MasterModule
from models.master_sub_module import MasterSubModule
from models.master_service import MasterService
from models.master_sub_service import MasterSubService
from models.master_sub_group import MasterSubGroup
from models.master_service_type import MasterServiceType
from models.user_registration import UserRegistration

from schemas.home_schema import (
    HomeServiceBase,
    HomeServiceCreate,
    HomeServiceUpdate,
    HomeServiceResponse,
    HomeServiceCreateResponse
)

from schemas.master_data_schema import MasterDataResponse

from services.home_service import (
    create_home_service,
    delete_home_service,
    get_home_service,
    get_home_services,
    update_home_service
)

from services.master_data_service import get_master_data

router = APIRouter(prefix="/api/master", tags=["Master Data & Bookings"])


@router.get("/master-data", response_model=MasterDataResponse)
def get_all_master_data(db: Session = Depends(get_db)):
    """Get all master data (modules, services, etc.)"""
    return get_master_data(db)


MODEL_MAP = {
    "module": MasterModule,
    "sub_module": MasterSubModule,
    "service": MasterService,
    "sub_service": MasterSubService,
    "sub_group": MasterSubGroup,
    "service_type": MasterServiceType,
}


@router.post("/master-data")
def create_master_data(type: str, data: dict, db: Session = Depends(get_db)):
    """Create master data"""
    ModelClass = MODEL_MAP.get(type)
    if not ModelClass:
        raise HTTPException(status_code=400, detail="Invalid type")

    obj = ModelClass(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/master-data/{id}")
def update_master_data(id: int, type: str, data: dict, db: Session = Depends(get_db)):
    """Update master data"""
    ModelClass = MODEL_MAP.get(type)
    if not ModelClass:
        raise HTTPException(400, "Invalid type")

    obj = db.query(ModelClass).filter(ModelClass.id == id).first()
    if not obj:
        raise HTTPException(404, "Not found")

    for key, value in data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/master-data/{id}")
def delete_master_data(id: int, type: str, db: Session = Depends(get_db)):
    """Delete master data"""
    ModelClass = MODEL_MAP.get(type)
    if not ModelClass:
        raise HTTPException(400, "Invalid type")

    obj = db.query(ModelClass).filter(ModelClass.id == id).first()
    if not obj:
        raise HTTPException(404, "Not found")

    db.delete(obj)
    db.commit()
    return {"message": "Deleted successfully"}


# ==================== HOME SERVICE BOOKING ====================

@router.get("/home-service", response_model=list[HomeServiceResponse])
def read_home_services(db: Session = Depends(get_db)):
    """Get all active home service bookings"""
    return get_home_services(db)


@router.get("/home-service/{id}", response_model=HomeServiceResponse)
def read_home_service_by_id(id: int, db: Session = Depends(get_db)):
    """Get a specific home service booking"""
    return get_home_service(db, id)


@router.post("/home-service", response_model=HomeServiceResponse)
def create_new_home_service(
    data: HomeServiceCreate,
    db: Session = Depends(get_db),
    current_user: UserRegistration = Depends(get_current_user)
):
    """
    Create a new home service booking.
    
    🔹 REQUIRED FIELDS:
    - module_id, sub_module_id, service_id, sub_service_id, sub_group_id
    - full_name, email, mobile (10 digits, starts with 6-9), address
    - service_type_id, duration_id
    - preferred_date, time_slot_id
    - payment_type_id, service_price
    
    🔹 OPTIONAL FIELDS:
    - issue_id, problem_description, property_size_sqft
    
    🔹 NOTES:
    - created_by is automatically set from authenticated user
    - status_id is automatically set to 1 (pending)
    - payment_done defaults to false
    """
    return create_home_service(db, data, current_user.id)


@router.put("/home-service/{id}", response_model=HomeServiceResponse)
def update_existing_home_service(
    id: int,
    data: HomeServiceUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing home service booking"""
    return update_home_service(db, id, data)


@router.delete("/home-service/{id}")
def remove_home_service(id: int, db: Session = Depends(get_db)):
    """Soft delete a home service booking"""
    return delete_home_service(db, id)
```

---

## 4. PAYMENT ROUTES - `controllers/payment_routes.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import razorpay
import os

from core.database import get_db
from models.home_service import HomeService

router = APIRouter(prefix="/api/payment", tags=["Payment"])

# ==================== RAZORPAY CLIENT ====================
client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET"),
    )
)


# ==================== REQUEST SCHEMAS ====================

class CreateOrderRequest(BaseModel):
    """Request to create a Razorpay order"""
    amount: int  # Amount in paisa (100 = 1 INR)
    bookingId: int  # HomeService ID


class VerifyPaymentRequest(BaseModel):
    """Request to verify payment signature"""
    order_id: str  # Razorpay order ID
    payment_id: str  # Razorpay payment ID
    signature: str  # Razorpay signature
    home_service_id: int  # HomeService ID to update


# ==================== PAYMENT ENDPOINTS ====================

@router.post("/create-order")
def create_order(req: CreateOrderRequest):
    """
    Create a Razorpay order.
    
    REQUEST BODY:
    {
        "amount": 50000,  // Amount in paisa (50000 = ₹500)
        "bookingId": 129
    }
    
    RESPONSE:
    {
        "id": "order_xxxxx",
        "entity": "order",
        "amount": 50000,
        "amount_paid": 0,
        "currency": "INR",
        "receipt": "receipt_129",
        ...
    }
    """
    try:
        order = client.order.create({
            "amount": req.amount,
            "currency": "INR",
            "receipt": f"receipt_{req.bookingId}",
        })
        return order
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create order: {str(e)}"
        )


@router.post("/verify-payment")
def verify_payment(
    req: VerifyPaymentRequest,
    db: Session = Depends(get_db)
):
    """
    Verify Razorpay payment signature and update booking as paid.
    
    REQUEST BODY:
    {
        "order_id": "order_xxxxx",
        "payment_id": "pay_xxxxx",
        "signature": "signature_xxxxx",
        "home_service_id": 129
    }
    
    RESPONSE:
    {
        "status": "success",
        "message": "Payment verified & booking updated",
        "booking_id": 129,
        "payment_done": true
    }
    
    ERRORS:
    - 400: Invalid Razorpay signature
    - 404: Booking not found
    """
    try:
        # 1️⃣ Verify Razorpay signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": req.order_id,
            "razorpay_payment_id": req.payment_id,
            "razorpay_signature": req.signature,
        })

        # 2️⃣ Get booking from database
        booking = db.get(HomeService, req.home_service_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        # 3️⃣ Mark payment as done
        booking.payment_done = True
        db.commit()
        db.refresh(booking)

        return {
            "status": "success",
            "message": "Payment verified & booking updated",
            "booking_id": booking.id,
            "payment_done": booking.payment_done,
        }

    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(
            status_code=400,
            detail="Invalid Razorpay signature - Payment verification failed"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Payment verification error: {str(e)}"
        )
```

---

## 5. MODEL - `models/home_service.py`

```python
from sqlalchemy import (
    BigInteger, Column, String, Boolean, Date, DateTime, ForeignKey, Integer, Numeric
)
from sqlalchemy.sql import func
from core.database import Base


class HomeService(Base):
    __tablename__ = "home_service"

    # ======================= PRIMARY KEY =======================
    id = Column(BigInteger, primary_key=True, index=True)

    # ======================= SERVICE HIERARCHY =======================
    module_id = Column(Integer, nullable=False)
    sub_module_id = Column(Integer, nullable=False)
    service_id = Column(BigInteger, nullable=False)
    sub_service_id = Column(Integer, nullable=False)
    sub_group_id = Column(BigInteger, nullable=False)

    # ======================= CUSTOMER DETAILS =======================
    full_name = Column(String(255), nullable=False)
    email = Column(String(150), nullable=False)
    mobile = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)

    # ======================= SERVICE DETAILS =======================
    service_type_id = Column(Integer, nullable=False)
    issue_id = Column(BigInteger)
    problem_description = Column(String(500))
    property_size_sqft = Column(String(150))
    duration_id = Column(Integer, nullable=False)

    # ======================= SCHEDULING =======================
    preferred_date = Column(Date, nullable=False)
    time_slot_id = Column(Integer, nullable=False)

    # ======================= PAYMENT =======================
    payment_type_id = Column(Integer, nullable=False)
    service_price = Column(Numeric(10, 2))
    payment_done = Column(Boolean, default=False)

    # ======================= SYSTEM FIELDS =======================
    created_by = Column(BigInteger, nullable=False)
    created_date = Column(DateTime, server_default=func.now())
    modified_by = Column(BigInteger)
    modified_date = Column(DateTime, onupdate=func.now())

    # ======================= ASSIGNMENT & STATUS =======================
    assigned_to = Column(BigInteger)  # Freelancer ID
    status_id = Column(Integer, nullable=False, default=1)
    rating = Column(Integer)  # Service rating (1-5)
    is_active = Column(Boolean, default=True)
```

---

## 6. COMPLETE API FLOW

### Step 1: Create Booking (without payment)
```
POST /api/master/home-service
Authorization: Bearer <token>

{
  "module_id": 1,
  "sub_module_id": 1,
  "service_id": 1,
  "sub_service_id": 1,
  "sub_group_id": 1,
  "full_name": "John Doe",
  "email": "john@example.com",
  "mobile": "9876543210",
  "address": "123 Main Street",
  "service_type_id": 1,
  "duration_id": 1,
  "preferred_date": "2026-01-15",
  "time_slot_id": 1,
  "payment_type_id": 1,
  "service_price": 500.00,
  "issue_id": null,
  "problem_description": null,
  "property_size_sqft": null
}

RESPONSE 200:
{
  "id": 129,
  "module_id": 1,
  "service_price": 500.0,
  "payment_done": false,
  "created_by": 5,
  "status_id": 1,
  "is_active": true,
  "created_date": "2026-01-10T10:30:00"
}
```

### Step 2: Create Razorpay Order
```
POST /api/payment/create-order

{
  "amount": 50000,
  "bookingId": 129
}

RESPONSE 200:
{
  "id": "order_1AHfqOvkldg2i4",
  "entity": "order",
  "amount": 50000,
  "amount_paid": 0,
  "currency": "INR",
  "receipt": "receipt_129",
  "status": "created",
  "attempts": 0,
  "notes": {},
  "created_at": 1673443534
}
```

### Step 3: Frontend - Razorpay Payment Gateway
Frontend captures payment using Razorpay checkout with:
- Key: `RAZORPAY_KEY_ID`
- Order ID: `order_1AHfqOvkldg2i4`
- Amount: ₹500
- Description: Service booking

### Step 4: Verify Payment & Update Booking
```
POST /api/payment/verify-payment

{
  "order_id": "order_1AHfqOvkldg2i4",
  "payment_id": "pay_1AHfqOvkldg2j5",
  "signature": "9ef4dffbfd84f1318f6739a3ce19f9d85851857ae648f114332d8401e0949a3d",
  "home_service_id": 129
}

RESPONSE 200:
{
  "status": "success",
  "message": "Payment verified & booking updated",
  "booking_id": 129,
  "payment_done": true
}
```

---

## 7. ENVIRONMENT VARIABLES

Add to `.env`:
```
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=xxxxx
```

---

## 8. FRONTEND INTEGRATION EXAMPLE (JavaScript)

```javascript
// 1. Create booking
const createBooking = async (bookingData, token) => {
  const response = await fetch('/api/master/home-service', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(bookingData)
  });
  return response.json();
};

// 2. Create Razorpay order
const createOrder = async (amount, bookingId) => {
  const response = await fetch('/api/payment/create-order', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount, bookingId })
  });
  return response.json();
};

// 3. Open Razorpay checkout
const openRazorpay = (order, bookingId) => {
  const options = {
    key: 'rzp_test_xxxxx',  // Your Razorpay Key ID
    amount: order.amount,
    currency: 'INR',
    name: 'Swachify India',
    description: 'Service Booking',
    order_id: order.id,
    handler: async (response) => {
      // Payment successful, verify signature
      await verifyPayment(response, bookingId);
    },
    prefill: {
      email: 'customer@example.com',
      contact: '9876543210'
    }
  };
  const razorpay = new Razorpay(options);
  razorpay.open();
};

// 4. Verify payment
const verifyPayment = async (razorpayResponse, bookingId) => {
  const response = await fetch('/api/payment/verify-payment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      order_id: razorpayResponse.razorpay_order_id,
      payment_id: razorpayResponse.razorpay_payment_id,
      signature: razorpayResponse.razorpay_signature,
      home_service_id: bookingId
    })
  });
  const result = await response.json();
  if (result.status === 'success') {
    alert('Payment successful!');
  }
};

// Full flow
const processBooking = async (bookingData, token) => {
  // Step 1: Create booking
  const booking = await createBooking(bookingData, token);
  
  // Step 2: Create order
  const order = await createOrder(
    Math.round(bookingData.service_price * 100),  // Convert to paisa
    booking.id
  );
  
  // Step 3: Open Razorpay
  openRazorpay(order, booking.id);
};
```

---

## 9. KEY NOTES

✅ **Payment Flow:**
1. Customer creates booking (status_id = 1, payment_done = false)
2. Frontend initiates Razorpay payment
3. After successful payment, backend verifies signature
4. Backend updates booking: payment_done = true

✅ **Status Codes:**
- 1 = Pending (default)
- 2 = Assigned
- 3 = In Progress
- 4 = Completed

✅ **Error Handling:**
- Invalid signature returns 400
- Missing booking returns 404
- Server errors return 500

✅ **Database Fields:**
- `payment_done`: Boolean flag (default: false)
- `service_price`: Decimal (amount to pay)
- `payment_type_id`: Type of payment (1 = Online, 2 = COD, etc.)

