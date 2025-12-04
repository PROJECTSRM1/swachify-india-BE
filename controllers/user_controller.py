from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from utils.db_function import execute_create_user_function
from schemas.user_schema import RegisterUser
from passlib.context import CryptContext
from utils.mail_agent import send_welcome_email
from utils.sms_agent import send_welcome_sms
import uuid
import re


pwd_context = CryptContext(
    schemes=["sha256_crypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def format_mobile(mobile: str) -> str:
    """
    Ensures only numbers & trims country codes if user enters +91 or spaces.
    """
    mobile = re.sub(r"\D", "", mobile)  # remove non-numeric

    if mobile.startswith("91") and len(mobile) == 12:
        mobile = mobile[2:]  # remove 91

    if len(mobile) != 10:
        raise HTTPException(status_code=400, detail="Invalid mobile number format")

    return mobile


def register_user_controller(db: Session, payload: RegisterUser, background_tasks: BackgroundTasks):

    # 1️⃣ Validate Password
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # 2️⃣ Sanitize mobile number
    mobile = format_mobile(payload.mobile)

    # 3️⃣ Generate Unique User ID
    generated_unique_id = str(uuid.uuid4())

    # 4️⃣ Prepare Parameters
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

    # 5️⃣ Execute Stored Procedure
    result = execute_create_user_function(db, params)
    if not result:
        raise HTTPException(status_code=500, detail="User creation failed")

    # 6️⃣ Trigger Notifications in Background
    background_tasks.add_task(send_welcome_email, payload.email, payload.first_name)
    background_tasks.add_task(send_welcome_sms, mobile, payload.first_name)

    # 7️⃣ Return Response
    return {
        "message": "User registered successfully",
        "notifications": "Welcome email and SMS queued",
        "data": dict(result._mapping)
    }
