import os
import uuid
import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
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


def freelancer_register_service(db: Session, payload)-> dict:
    """
    Register a freelancer with full auto-default master lookup
    and JSON-packed government ID storage.
    """
    if db.query(UserRegistration).filter(UserRegistration.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    if db.query(UserRegistration).filter(UserRegistration.mobile == payload.mobile).first():
        raise HTTPException(status_code=400, detail="Mobile already exists")

    state = fetch_default_state(db) if not payload.state_id else None
    district = fetch_default_district(db,state.id) if state and not payload.district_id else None
    skill = fetch_default_skill(db) if not payload.skill_id else None
    gender_id = payload.gender_id if payload.gender_id not in (None, 0) else None
    if not gender_id:
        default_gender = fetch_default_gender(db)
        if not default_gender:
            raise HTTPException(status_code=500, detail="No default gender found in master table")
        gender_id = default_gender.id

 
    government_json = None
    if payload.government_id_type and payload.government_id_number:
        government_json = json.dumps({
            "type": payload.government_id_type,
            "number": payload.government_id_number
        })

    freelancer = UserRegistration(
        first_name = payload.first_name,
        last_name = payload.last_name,
        email = payload.email,
        mobile = payload.mobile,
        password = hash_password(payload.password),
        gender_id = gender_id,
        state_id = payload.state_id or (state.id if state else None),
        district_id = payload.district_id or (district.id if district else None),
        skill_id = payload.skill_id or (skill.id if skill else None),
        role_id=FREELANCER_ROLE_ID,
        status_id=STATUS_PENDING,  
        is_active=True, 
        government_id=government_json,
        address = payload.address,
        unique_id = str(uuid.uuid4()),
        experience_summary = payload.experience_summary,
        experience_doc = payload.experience_doc
    )

    try:
        db.add(freelancer)
        db.commit()
        db.refresh(freelancer)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error registering freelancer") from e
    
    return {
        "message": "Freelancer registered successfully. Waiting for admin approval.",
        "user_id": freelancer.id,
        "status": "Pending"
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

    service = db.query(HomeService).filter(
        HomeService.id == service_id,
        HomeService.assigned_to == freelancer_id,
        HomeService.status_id == STATUS_ASSIGNED
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found or not assigned to this freelancer"
        )

    service.status_id = STATUS_COMPLETED
    service.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(service)

    return {
        "message": "Service marked as completed successfully",
        "service_id": service.id,
        "status_id": STATUS_COMPLETED,
        "status_name": "Completed",
        "freelancer_id": freelancer_id
    }
