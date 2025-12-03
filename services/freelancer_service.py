from fastapi import HTTPException
from sqlalchemy.orm import Session
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


def freelancer_register_service(db: Session, payload):
    """
    Register a freelancer with full auto-default master lookup
    and JSON-packed government ID storage.
    """
    # Unique email
    if db.query(UserRegistration).filter(UserRegistration.email == payload.email).first():
        raise HTTPException(400, "Email already exists")

    # Unique mobile
    if db.query(UserRegistration).filter(UserRegistration.mobile == payload.mobile).first():
        raise HTTPException(400, "Mobile already exists")

    # Default values from master tables
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
        role_id = FREELANCER_ROLE_ID,
        government_id=government_json,
        address = payload.address,
        unique_id = str(uuid.uuid4())
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Freelancer registered successfully",
        "user_id": user.id
    }

def freelancer_login_service(db: Session, payload):

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


    subject = {
        "user_id": user.id,
        "email": user.email,
        "role": "freelancer"
    }

    return {
        "message":"Login Successful",
        "user_id": user.id,
        "email_or_phone": identifier
    }
