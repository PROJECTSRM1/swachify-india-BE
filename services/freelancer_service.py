import os
import uuid
import json
from fastapi import HTTPException
from pydantic import validate_call
from sqlalchemy.orm import Session
from datetime import datetime
from services.role_service import validate_role
from utils.jwt_utils import create_access_token,create_refresh_token
from models.user_registration import UserRegistration
from models.home_service import HomeService
from utils.hash_utils import hash_password,verify_password
from services.master_default_service import (
    fetch_default_skill,
    fetch_default_state,
    fetch_default_district,
    fetch_default_gender
)


FREELANCER_ROLE_ID = 4

#freelancer status IDs
STATUS_APPROVED = 1
STATUS_PENDING = 2
STATUS_REJECTED = 3

#🔹 FREELANCER SERVICES🔹#
STATUS_ASSIGNED = 4
STATUS_NOT_ASSIGNED = 5
STATUS_COMPLETED = 6


def freelancer_register_service(db: Session, payload) -> dict:

    if db.query(UserRegistration).filter(UserRegistration.email == payload.email).first():
        raise HTTPException(400, "Email already exists")

    if db.query(UserRegistration).filter(UserRegistration.mobile == payload.mobile).first():
        raise HTTPException(400, "Mobile already exists")

    # ✅ Validate role
    role = validate_role(db, payload.role_id)

    # ✅ Government ID JSON
    government_id = None
    if payload.government_id_type and payload.government_id_number:
        government_id = {
            "type": payload.government_id_type,
            "number": payload.government_id_number,
            "verified": False
        }

    user = UserRegistration(
        unique_id=str(uuid.uuid4()),
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        mobile=payload.mobile,
        password=hash_password(payload.password),

        role_id=role.id,
        status_id=STATUS_PENDING,
        is_active=True,

        gender_id=payload.gender_id,
        state_id=payload.state_id,
        district_id=payload.district_id,
        skill_id=payload.skill_id,

        address=payload.address,
        government_id=government_id,

        experience_summary=payload.experience_summary,
        experience_doc=payload.experience_doc
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token_payload = {
        "user_id": str(user.id),
        "role_id": role.id,
        "role": role.role_name,
        "status": "pending"
    }

    return {
        "message": "User registered successfully. Awaiting admin approval.",
        "user_id": user.id,
        "role": role.role_name,
        "access_token": create_access_token(token_payload),
        "refresh_token": create_refresh_token(token_payload),
        "token_type": "bearer",
        "expires_in": int(os.getenv("JWT_EXPIRE_MINUTES", 15)) * 60
    }


def freelancer_login_service(db: Session, payload, response) -> dict:

    identifier = payload.email_or_phone.strip()

    query= db.query(UserRegistration).filter(
        UserRegistration.role_id == FREELANCER_ROLE_ID, 
        UserRegistration.is_active == True
    )

    freelancer = (
        query.filter(UserRegistration.email == identifier).first()
        if "@" in identifier else
        query.filter(UserRegistration.mobile == identifier).first()
    )

    if not freelancer:
        raise HTTPException(404, "Freelancer not found")

    if not verify_password(payload.password, freelancer.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    
    if freelancer.status_id == STATUS_PENDING:
        raise HTTPException(
            status_code=403,
            detail="Your account is pending, wait for admin actions"
        )

    if freelancer.status_id == STATUS_REJECTED:
        raise HTTPException(
            status_code=403,
            detail="Your account has been rejected by admin"
        )


    subject = {
        "user_id": str(freelancer.id),
        "email": freelancer.email,
        "role": "freelancer"
    }

    access_token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)

    refresh_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    response.set_cookie(
        key="freelancer_refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=refresh_days * 86400,
    )

    return {
        "message": "Freelancer login successful",
        "user_id": freelancer.id,
        "email_or_phone": identifier,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": int(os.getenv("JWT_EXPIRE_MINUTES", 15)) * 60
    }

def get_freelancer_by_id(db: Session, freelancer_id: int)-> dict:

    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active == True
    ).first()

    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer not found")
    
    if freelancer.status_id == STATUS_PENDING:
        raise HTTPException(
            status_code=403,
            detail="Freelancer profile is still pending, wait  admin approval"
        )
    
    if freelancer.status_id == STATUS_REJECTED:
        raise HTTPException(
            status_code=403,
            detail="Freelancer profile has been rejected by admin"
        )
    
    if freelancer.status_id != STATUS_APPROVED:
        raise HTTPException(
            status_code=403,
            detail="Freelancer profile is not approved by admin"
        )
    
    return {
        "message": "Freelancer fetched successfully",
        "freelancer_id": freelancer.id,
        "first_name": freelancer.first_name,
        "last_name": freelancer.last_name,
        "email": freelancer.email,
        "mobile": freelancer.mobile,
        "gender_id": freelancer.gender_id,
        "state_id": freelancer.state_id,
        "district_id": freelancer.district_id,
        "skill_id": freelancer.skill_id,
        "address": freelancer.address,
        "status_id": freelancer.status_id,
        "created_date": freelancer.created_date
    }

def freelancer_update_service(db: Session, freelancer_id: int, payload):

    freelancer= db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active == True
    ).first()

    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer not found")

    if freelancer.status_id != STATUS_APPROVED:
        raise HTTPException(
            status_code=403,
            detail="Profile update allowed only after admin approval"
        )

    for field in ["first_name", "last_name", "email", "mobile", "address"]:
        value=getattr(payload, field, None)
        if value:
            setattr(freelancer, field, value)

    if payload.password:
        freelancer.password = hash_password(payload.password)

    db.commit()
    db.refresh(freelancer)

    return {"message": "Freelancer updated successfully", "freelancer_id": freelancer.id}



def freelancer_delete_service(db: Session, freelancer_id: int)-> dict:

    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID
    ).first()

    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer not found")

    db.delete(freelancer)
    db.commit()

    return {"message": "Freelancer deleted successfully"}

def freelancer_status_service(db: Session, freelancer_id: int)-> dict:

    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active == True
    ).first()

    if not freelancer:
        raise HTTPException(404, "Freelancer not found")

    status_map = {
        STATUS_PENDING: "Pending",
        STATUS_APPROVED: "Approved",
        STATUS_REJECTED: "Rejected"
    }

    message_map = {
        STATUS_PENDING: "Your account is pending, wait for admin actions",
        STATUS_APPROVED: "Your account has been approved by admin",
        STATUS_REJECTED: "Your account has been rejected by admin"
    }

    return {
        "freelancer_id": freelancer.id,
        "status": status_map.get(freelancer.status_id),
        "message": message_map.get(freelancer.status_id)
    }

def freelancer_complete_job_service(
    db: Session,
    freelancer_id: int,
    service_id: int
) -> dict:
    """
    Freelancer marks assigned home service as completed
    """

    service = (
        db.query(HomeService)
        .filter(HomeService.id == service_id)
        .with_for_update()
        .first()
    )

    # 1️⃣ Service does not exist
    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    # 2️⃣ Service exists but not assigned
    if not service.assigned_to:
        raise HTTPException(
            status_code=400,
            detail="Service is not yet assigned to any freelancer"
        )

    # 3️⃣ Assigned to another freelancer
    if service.assigned_to != freelancer_id:
        raise HTTPException(
            status_code=403,
            detail="Service is assigned to another freelancer"
        )

    # 4️⃣ Already completed
    if service.status_id == STATUS_COMPLETED:
        raise HTTPException(
            status_code=409,
            detail="Service is already marked as completed"
        )

    # 5️⃣ Not in assigned state
    if service.status_id != STATUS_ASSIGNED:
        raise HTTPException(
            status_code=400,
            detail="Service cannot be completed in its current state"
        )

    # ✅ Valid completion
    service.status_id = STATUS_COMPLETED
    service.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(service)

    return {
        "message": "Service marked as completed successfully",
        "service_id": service.id,
        "previous_status": STATUS_ASSIGNED,
        "current_status": STATUS_COMPLETED,
        "status_name": "Completed",
        "completed_by": freelancer_id,
        "completed_at": service.modified_date
    }
