import os
from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils.jwt_utils import create_access_token,create_refresh_token
from models.user_registration import UserRegistration
from utils.hash_utils import hash_password,verify_password
from services.master_default_service import (
    fetch_default_skill,
    fetch_default_state,
    fetch_default_district,
    fetch_default_gender
)
import uuid
import json


FREELANCER_ROLE_ID = 4

STATUS_APPROVED = 1
STATUS_PENDING = 2
STATUS_REJECTED = 3



def freelancer_register_service(db: Session, payload):
    """
    Register a freelancer with full auto-default master lookup
    and JSON-packed government ID storage.
    """
    if db.query(UserRegistration).filter(UserRegistration.email == payload.email).first():
        raise HTTPException(400, "Email already exists")

    if db.query(UserRegistration).filter(UserRegistration.mobile == payload.mobile).first():
        raise HTTPException(400, "Mobile already exists")

    state = fetch_default_state(db) if not payload.state_id else None
    district = fetch_default_district(db,state.id) if state and not payload.district_id else None
    skill = fetch_default_skill(db) if not payload.skill_id else None
    gender_id = payload.gender_id if payload.gender_id not in (None, 0) else None
    if not gender_id:
        default_gender = fetch_default_gender(db)
        if not default_gender:
            raise HTTPException(500, "No default gender found in master table")
        gender_id = default_gender.id

 
    government_json = None
    if payload.government_id_type and payload.government_id_number:
        government_json = json.dumps({
            "type": payload.government_id_type,
            "number": payload.government_id_number
        })

    user = UserRegistration(
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
        government_id=government_json,
        address = payload.address,
        unique_id = str(uuid.uuid4()),
        experience_summary = payload.experience_summary,
        experience_doc = payload.experience_doc
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Freelancer registered successfully. Waiting for admin approval.",
        "user_id": user.id,
        "status": "Pending"
    }


def freelancer_login_service(db: Session, payload, response):

    identifier = payload.email_or_phone.strip()

    if "@" in identifier:
        user = db.query(UserRegistration).filter(
            UserRegistration.email == identifier,
            UserRegistration.role_id == FREELANCER_ROLE_ID
        ).first()
    else:
        user = db.query(UserRegistration).filter(
            UserRegistration.mobile == identifier,
            UserRegistration.role_id == FREELANCER_ROLE_ID
        ).first()

    if not user:
        raise HTTPException(404, "Freelancer not found")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    # ---- STATUS ENFORCEMENT ----
    if user.status_id == STATUS_PENDING:
        raise HTTPException(
            status_code=403,
            detail="Your account is pending, wait for admin actions"
        )

    if user.status_id == STATUS_REJECTED:
        raise HTTPException(
            status_code=403,
            detail="Your account has been rejected by admin"
        )


    subject = {
        "user_id": user.id,
        "email": user.email,
        "role": "freelancer"
    }

    access_token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)

    refresh_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    max_age = refresh_days * 24 * 3600

    response.set_cookie(
        key="freelancer_refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=max_age
    )

    return {
        "message": "Freelancer login successful",
        "user_id": user.id,
        "email_or_phone": identifier,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": int(os.getenv("JWT_EXPIRE_MINUTES", 15)) * 60
    }

def get_freelancer_by_id(db: Session, freelancer_id: int):
    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.status_id == STATUS_APPROVED,
        UserRegistration.is_active == True
    ).first()

    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer not found")
    
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
        "is_active": freelancer.is_active,
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


    freelancer.first_name = payload.first_name or freelancer.first_name
    freelancer.last_name = payload.last_name or freelancer.last_name
    freelancer.email = payload.email or freelancer.email
    freelancer.mobile = payload.mobile or freelancer.mobile
    freelancer.address = payload.address or freelancer.address
    if payload.password:
        freelancer.password = hash_password(payload.password)

    if freelancer.status_id != STATUS_APPROVED:
        raise HTTPException(
            status_code=403,
            detail="Profile update allowed only after admin approval"
        )

    db.commit()
    db.refresh(freelancer)

    return {"message": "Freelancer updated successfully", "freelancer_id": user.id}



def freelancer_delete_service(db: Session, freelancer_id: int):

    user = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Freelancer not found")

    db.delete(user)
    db.commit()

    return {"message": "Freelancer deleted successfully"}

def freelancer_status_service(db: Session, freelancer_id: int):

    user = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID
    ).first()

    if not user:
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
        "freelancer_id": user.id,
        "status": status_map.get(user.status_id),
        "message": message_map.get(user.status_id)
    }

