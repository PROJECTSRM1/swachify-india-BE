import os
import uuid
import json
from fastapi import HTTPException
from pydantic import validate_call
from sqlalchemy.orm import Session
from datetime import datetime
from services.role_service import validate_role
from utils.jwt_utils import create_access_token, create_refresh_token
from models.generated_models import UserRegistration,HomeServiceBooking,UserSkill,UserServices
from utils.hash_utils import hash_password, verify_password
from services.master_default_service import (
    fetch_default_skill,
    fetch_default_state,
    fetch_default_district,
    fetch_default_gender
)
from core.constants import (
    FREELANCER_ROLE_ID,
    STATUS_APPROVED,
    STATUS_PENDING,
    STATUS_REJECTED,
    STATUS_ASSIGNED,
    WORK_STATUS_JOB_COMPLETED,
)


def freelancer_login_service(db: Session, payload, response) -> dict:
    """
    Authenticate freelancer and generate JWT tokens.
    Only allows login for APPROVED freelancers (status_id=1).
    
    Args:
        db: Database session
        payload: LoginRequest with email_or_phone and password
        response: FastAPI response for setting cookies
    
    Returns:
        Dictionary with tokens and user information
    """

    identifier = payload.email_or_phone.strip()

    query = db.query(UserRegistration).filter(
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
    
    # Explicitly require APPROVED status (status_id=1)
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
    
    if freelancer.status_id != STATUS_APPROVED:
        raise HTTPException(
            status_code=403,
            detail="Your account has not been approved by admin"
        )


    subject = {
        "user_id": str(freelancer.id),
        "email": freelancer.email,
        "role_id": freelancer.role_id
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

def get_freelancer_by_id(db: Session, freelancer_id: int) -> dict:
    """
    Fetch freelancer details including skills. Only accessible if APPROVED.
    
    Args:
        db: Database session
        freelancer_id: ID of freelancer to fetch
    
    Returns:
        Dictionary with freelancer profile and skills
    """

    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active == True
    ).first()

    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer not found")
    
    # Explicitly require APPROVED status
    if freelancer.status_id == STATUS_PENDING:
        raise HTTPException(
            status_code=403,
            detail="Freelancer profile is still pending, wait for admin approval"
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
    
    # Fetch all skill_ids for this freelancer
    skill_ids = [s.skill_id for s in db.query(UserSkill).filter_by(user_id=freelancer.id).all()]
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
        "skill_ids": skill_ids,
        "address": freelancer.address,
        "status_id": freelancer.status_id,
        "created_date": freelancer.created_date
    }

def freelancer_update_service(db: Session, freelancer_id: int, payload) -> dict:
    """
    Update freelancer profile. Only allowed for APPROVED freelancers.
    
    Args:
        db: Database session
        freelancer_id: ID of freelancer to update
        payload: Update request with optional fields
    
    Returns:
        Dictionary with success message
    """

    freelancer = db.query(UserRegistration).filter(
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



def freelancer_delete_service(db: Session, freelancer_id: int) -> dict:
    """
    Delete freelancer account and associated data.
    
    Args:
        db: Database session
        freelancer_id: ID of freelancer to delete
    
    Returns:
        Dictionary with success message
    """

    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID
    ).first()

    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer not found")

    # Delete related UserServices
    db.query(UserServices).filter(UserServices.user_id == freelancer_id).delete()
    # Delete related UserSkill
    db.query(UserSkill).filter(UserSkill.user_id == freelancer_id).delete()
    # (Add more related deletes here if needed)

    db.delete(freelancer)
    db.commit()

    return {"message": "Freelancer deleted successfully"}

def freelancer_status_service(db: Session, freelancer_id: int) -> dict:
    """
    Get freelancer account status with human-readable message.
    
    Args:
        db: Database session
        freelancer_id: ID of freelancer
    
    Returns:
        Dictionary with status and status message
    """

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
        db.query(HomeServiceBooking)
        .filter(HomeServiceBooking.id == service_id)
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

    # 4️⃣ Not in assigned state
    if service.status_id != STATUS_ASSIGNED:
        raise HTTPException(
            status_code=400,
            detail="Service cannot be completed in its current state"
        )

    # 5️⃣ Check if already completed
    if service.work_status_id == WORK_STATUS_JOB_COMPLETED:
        raise HTTPException(
            status_code=409,
            detail="Service is already completed and cannot be completed again"
        )

    # ✅ Valid completion - Update status and mark completion time
    service.work_status_id = WORK_STATUS_JOB_COMPLETED
    service.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(service)

    return {
        "message": "Service Completed successfully",
        "service_id": service.id,
        "status": "Completed",
        "completed_by": freelancer_id,
        "completed_at": service.modified_date
    }
