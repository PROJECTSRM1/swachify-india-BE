from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from models.user_registration import UserRegistration
from schemas.admin_schema import RegisterAdmin,AdminLogin,AdminLogout,UserBase,AdminRegisterResponse
from utils.hash_utils import hash_password,verify_password
from utils.jwt_utils import create_access_token,create_refresh_token,is_admin_already_logged_in
import uuid
import os
from sqlalchemy import or_
from datetime import datetime

ADMIN_ROLE_ID = 1
FREELANCER_ROLE_ID = 4

STATUS_APPROVED = 1
STATUS_PENDING = 2
STATUS_REJECTED = 3

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
        role_id=1,
        is_active=True,
        unique_id = str(uuid.uuid4())
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return {
        "message": "Admin registered successfully",
        "data": admin
    }

def admin_login_service(credentials: AdminLogin, db: Session):
    
    identifier = credentials.username_or_email.strip()
    
    admin = db.query(UserRegistration).filter(
        UserRegistration.role_id == ADMIN_ROLE_ID,
        UserRegistration.is_active == True,
        or_(
            UserRegistration.email == identifier,
            UserRegistration.mobile == identifier,
            UserRegistration.unique_id == identifier
        )
    ).first()

    if not admin or not verify_password(credentials.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
    "user_id": admin.id,
    "email": admin.email,
    "role": "admin"
    }

    
    user_data = UserBase.model_validate(admin)

    return {
        "message": "Login successful",
        "user": user_data,
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer",
    }

def admin_me_service(current_admin: UserRegistration):
    user_data = UserBase.model_validate(current_admin)

    return {
        "message": "Admin details fetched successfully",
        "data": user_data
    }

def admin_update_service(
    db: Session,
    current_admin: UserRegistration,
    payload: dict
):
   
    # Whitelisted fields ONLY
    allowed_fields = {
        "first_name",
        "last_name",
        "address"
    }

    for field in allowed_fields:
        if field in payload and payload[field] is not None:
            setattr(current_admin, field, payload[field])

    current_admin.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(current_admin)

    return {
        "message": "Admin details updated successfully",
        "data": {
            "id": current_admin.id,
            "first_name": current_admin.first_name,
            "last_name": current_admin.last_name,
            "email": current_admin.email,
            "mobile": current_admin.mobile,
            "address": current_admin.address
        }
    }

def admin_deactivate_service(
    db: Session,
    current_admin: UserRegistration
  ):
    
    current_admin.is_active = False
    current_admin.modified_date = datetime.utcnow()

    db.commit()

    return {"message": "Admin deactivated successfully"}

def activate_admin_service(
    db: Session,
    admin_id: int
):
    admin = db.query(UserRegistration).filter(
        UserRegistration.id == admin_id,
        UserRegistration.role_id == ADMIN_ROLE_ID,
        UserRegistration.is_active == False
    ).first()

    if not admin:
        raise HTTPException(404, "Inactive admin not found")

    admin.is_active = True
    admin.modified_by = admin_id
    admin.modified_date = datetime.utcnow()

    db.commit()

    return {"message": "Admin activated successfully"}


def activate_freelancer_service(
    db: Session,
    freelancer_id: int,
    admin_id: int
):
    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active == False
    ).first()

    if not freelancer:
        raise HTTPException(404, "Inactive freelancer not found")

    freelancer.is_active = True
    freelancer.modified_by = admin_id
    freelancer.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(freelancer)

    return {
        "message": "Freelancer account activated successfully",
        "freelancer_id": freelancer.id,
        "active": True
    }



def get_pending_freelancers_service(db: Session):

    return db.query(UserRegistration).filter(
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.status_id == STATUS_PENDING,
        UserRegistration.is_active == True
    ).all()


def approve_freelancer_service(db: Session, freelancer_id: int, admin_id: int):
   
    user = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.status_id == STATUS_PENDING,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(404, "Pending Freelancer not found")

    user.status_id = STATUS_APPROVED
    user.modified_by = admin_id
    user.modified_date = datetime.utcnow()


    db.commit()
    db.refresh(user)

    return {
        "message": "Freelancer approved successfully",
        "freelancer_id": user.id,
        "status": "Approved"
    }


def reject_freelancer_service(db: Session, freelancer_id: int, admin_id: int):
    user = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.status_id == STATUS_PENDING,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(404, "Pending Freelancer not found")
    
    user.status_id = STATUS_REJECTED
    user.modified_by = admin_id
    user.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return {
        "message": "Freelancer rejected",
        "freelancer_id": user.id,
        "status": "Rejected"
    }