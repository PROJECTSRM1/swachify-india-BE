from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from sqlalchemy import or_
from models.generated_models import UserRegistration,HomeService
from schemas.admin_schema import RegisterAdmin, AdminLogin, UserBase
from utils.hash_utils import hash_password, verify_password
from utils.jwt_utils import create_access_token, create_refresh_token, is_admin_already_logged_in
from core.constants import (
    ADMIN_ROLE_ID,
    CUSTOMER_ROLE_ID,
    FREELANCER_ROLE_ID,
    STATUS_APPROVED,
    STATUS_PENDING,
    STATUS_REJECTED,
    STATUS_ASSIGNED,
    STATUS_NOT_ASSIGNED
)
import uuid
from datetime import datetime

# Service completion status (mapped to master_status or work_status)
STATUS_COMPLETED = 6

def register_admin_service(request: RegisterAdmin, db: Session):

    if db.query(UserRegistration).filter(UserRegistration.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    if db.query(UserRegistration).filter(UserRegistration.mobile == request.mobile).first():
        raise HTTPException(status_code=400, detail="Mobile number already exists")

    admin = UserRegistration(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        mobile=request.mobile,
        password=hash_password(request.password),
        gender_id=request.gender_id,
        address=request.address,
        role_id=ADMIN_ROLE_ID,
        status_id=STATUS_APPROVED,
        created_date=datetime.utcnow(),
        is_active=True,
        unique_id=str(uuid.uuid4())
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    # ✅ RETURN ORM OBJECT
    return {
        "message": "Admin registered successfully",
        "data": admin
    }

def admin_login_service(credentials: AdminLogin, db: Session, http_request: Request):
    """
    Authenticate admin and generate JWT tokens.
    
    Args:
        credentials: Admin login credentials (email/mobile/unique_id + password)
        db: Database session
        http_request: HTTP request for checking existing sessions
    
    Returns:
        Dictionary with tokens and admin info
    
    Raises:
        HTTPException: If already logged in or credentials invalid
    """
    if is_admin_already_logged_in(http_request):
        return {
            "status": "warning",
            "code": 409,
            "message": "Admin already logged in. Please logout to login again."
        }

    identifier = credentials.username_or_email.strip()

    admin = db.query(UserRegistration).filter(
        UserRegistration.role_id == ADMIN_ROLE_ID,
        UserRegistration.is_active == True,
        or_(
            UserRegistration.email == identifier,
            UserRegistration.mobile == identifier,
            UserRegistration.unique_id == identifier,
        )
    ).first()

    if not admin or not verify_password(credentials.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # JWT token with role_id (consistent with freelancer and auth_dependencies)
    payload = {
        "user_id": str(admin.id),
        "email": admin.email,
        "role_id": admin.role_id
    }

    return {
        "message": "Login successful",
        "user": UserBase.model_validate(admin),
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer",
    }



def admin_update_service(db: Session, admin_id: int, payload: dict):
    """
    Update admin profile information.
    
    Args:
        db: Database session
        admin_id: ID of admin to update
        payload: Dictionary with fields to update
    
    Returns:
        Dictionary with success message and updated admin
    
    Raises:
        HTTPException: If admin not found or email/mobile duplicate
    """
    admin = db.query(UserRegistration).filter(
        UserRegistration.id == admin_id,
        UserRegistration.role_id == ADMIN_ROLE_ID
    ).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    if "email" in payload and payload["email"] != admin.email:
        existing_email = db.query(UserRegistration).filter(
            UserRegistration.email == payload["email"],
            UserRegistration.id != admin_id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")

    if "mobile" in payload and payload["mobile"] != admin.mobile:
        existing_mobile = db.query(UserRegistration).filter(
            UserRegistration.mobile == payload["mobile"],
            UserRegistration.id != admin_id
        ).first()
        if existing_mobile:
            raise HTTPException(status_code=400, detail="Mobile number already exists")

    for key, value in payload.items():
        if key == "password":
            value = hash_password(value)
        setattr(admin, key, value)

    admin.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(admin)
    return {
        "message": "Admin details updated successfully",
        "data": admin
    }


def admin_delete_service(db: Session, admin_id: int):
    """
    Soft delete (deactivate) an admin user.
    
    Args:
        db: Database session
        admin_id: ID of admin to deactivate
    
    Returns:
        Dictionary with success message
    
    Raises:
        HTTPException: If admin not found
    """
    admin = db.query(UserRegistration).filter(
        UserRegistration.id == admin_id,
        UserRegistration.role_id == ADMIN_ROLE_ID,
        UserRegistration.is_active == True
    ).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    admin.is_active = False
    admin.modified_date = datetime.utcnow()

    db.commit()
    return {"message": "Admin deactivated successfully"}

def admin_hard_delete_service(db: Session, admin_id: int):
    admin = db.query(UserRegistration).filter(
        UserRegistration.id == admin_id,
        UserRegistration.role_id == ADMIN_ROLE_ID
    ).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    db.delete(admin)
    db.commit()
    return {"message": "Admin deleted permanently"}

def get_pending_freelancers_service(db: Session):
    return db.query(UserRegistration).filter(
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.status_id == STATUS_PENDING,
        UserRegistration.is_active == True
    ).all()


def approve_freelancer_service(db: Session, freelancer_id: int, admin_id: int):
    """
    Approve a PENDING freelancer (status: PENDING → APPROVED).
    Uses row-level locking to prevent race conditions.
    
    Args:
        db: Database session
        freelancer_id: ID of freelancer to approve
        admin_id: ID of admin approving
    
    Returns:
        Dictionary with success message and freelancer info
    
    Raises:
        HTTPException: If freelancer not found or not in PENDING status
    """
    freelancer = (
        db.query(UserRegistration).filter(
            UserRegistration.id == freelancer_id,
            UserRegistration.role_id == FREELANCER_ROLE_ID,
            UserRegistration.status_id == STATUS_PENDING,
            UserRegistration.is_active == True
        )
        .with_for_update()
        .first()
    )

    if not freelancer:
        raise HTTPException(status_code=409, detail="Freelancer already processed or not found")

    freelancer.status_id = STATUS_APPROVED
    freelancer.modified_by = admin_id
    freelancer.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(freelancer)

    return {
        "message": "Freelancer approved successfully",
        "freelancer_id": freelancer.id,
        "approved_by": admin_id
    }


def reject_freelancer_service(db: Session, freelancer_id: int, admin_id: int):
    """
    Reject a PENDING freelancer (status: PENDING → REJECTED).
    Uses row-level locking to prevent race conditions.
    
    Args:
        db: Database session
        freelancer_id: ID of freelancer to reject
        admin_id: ID of admin rejecting
    
    Returns:
        Dictionary with success message and freelancer info
    
    Raises:
        HTTPException: If freelancer not found or not in PENDING status
    """
    freelancer = (
        db.query(UserRegistration).filter(
            UserRegistration.id == freelancer_id,
            UserRegistration.role_id == FREELANCER_ROLE_ID,
            UserRegistration.status_id == STATUS_PENDING,
            UserRegistration.is_active == True
        )
        .with_for_update()
        .first()
    )

    if not freelancer:
        raise HTTPException(status_code=409, detail="Freelancer already processed or not found")

    freelancer.status_id = STATUS_REJECTED
    freelancer.modified_by = admin_id
    freelancer.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(freelancer)

    return {
        "message": "Freelancer rejected successfully",
        "freelancer_id": freelancer.id,
        "rejected_by": admin_id
    }
    
def get_all_customers_service(db: Session):
    """
    Fetch all active customers (role_id = 2).
    
    Args:
        db: Database session
    
    Returns:
        List of customer records
    """
    customers = db.query(UserRegistration).filter(
        UserRegistration.role_id == CUSTOMER_ROLE_ID,
        UserRegistration.is_active == True
    ).all()
    
    return customers


def get_customer_details_service(db: Session, customer_id: int):
    """
    Fetch complete customer profile details.
    
    Args:
        db: Database session
        customer_id: Customer user ID
    
    Returns:
        Dictionary with customer details
    
    Raises:
        HTTPException: If customer not found
    """
    customer = db.query(UserRegistration).filter(
        UserRegistration.id == customer_id,
        UserRegistration.role_id == CUSTOMER_ROLE_ID
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Import here to avoid circular imports
    from models.generated_models import MasterGender
    from models.generated_models import MasterState
    from models.generated_models import MasterDistrict
    
    state_name = db.query(MasterState.state_name).filter(
        MasterState.id == customer.state_id
    ).scalar() if customer.state_id else None
    
    district_name = db.query(MasterDistrict.district_name).filter(
        MasterDistrict.id == customer.district_id
    ).scalar() if customer.district_id else None
    
    gender_value = db.query(MasterGender.gender_name).filter(
        MasterGender.id == customer.gender_id
    ).scalar() if customer.gender_id else None
    
    response = {
        "user_id": customer.id,
        "full_name": f"{customer.first_name} {customer.last_name or ''}".strip(),
        "mobile": customer.mobile,
        "email": customer.email,
        "gender": gender_value,
        "state": state_name,
        "district": district_name,
        "address": customer.address,
        "status": "active" if customer.is_active else "inactive",
        "created_date": customer.created_date.isoformat() if customer.created_date else None
    }
    
    return {
        "status": "success",
        "code": 200,
        "message": "Customer details fetched successfully",
        "data": response
    }



#rajashekar