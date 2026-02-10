from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from utils.db_function import execute_create_user_function
from schemas.user_schema import RegisterUser
from passlib.context import CryptContext
import uuid
import re

pwd_context = CryptContext(schemes=["sha256_crypt"],deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def format_mobile(mobile: str) -> str:
    mobile = re.sub(r"\D", "", mobile)
    if mobile.startswith("91") and len(mobile) == 12:
        mobile = mobile[2:]
    if len(mobile) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid mobile number format"
        )
    return mobile

async def register_user_controller(db: Session, payload: RegisterUser):
    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    mobile = format_mobile(payload.mobile)
    generated_unique_id = str(uuid.uuid4())
    params = {
        "p_unique_id": generated_unique_id,
        "p_first_name": payload.first_name,
        "p_last_name": payload.last_name,
        "p_email": payload.email,
        "p_mobile": mobile,
        "p_password": hash_password(payload.password),
        "p_gender_id": payload.gender_id,
        "p_dob": None,
        "p_age": None,
        "p_role_id": None,
        "p_state_id": None,
        "p_district_id": None,
        "p_created_by": None,
        "p_profile_image": None,
        "p_skill_id": None,
        "p_experience_summary": None,
        "p_experience_doc": None,
        "p_government_id": None,
        "p_address": payload.address
    }

    result = execute_create_user_function(db, params)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    return {
        "user_id": result.id if hasattr(result, "id") else result[0]
    }
