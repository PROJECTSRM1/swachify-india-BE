from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.db_function import execute_create_user_function
from utils.hash import hash_password
from schemas.user_schema import RegisterUser


def register_user_controller(db: Session, payload: RegisterUser):

    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    params = {
        "p_first_name": payload.first_name,
        "p_last_name": payload.last_name or "",
        "p_email": payload.email,
        "p_mobile": payload.mobile,
        "p_password": hash_password(payload.password),
        "p_gender_id": payload.gender_id,
        "p_unique_id": payload.unique_id,
        "p_dob": payload.dob,
        "p_age": payload.age,
        "p_role_id": payload.role_id,
        "p_state_id": payload.state_id,
        "p_district_id": payload.district_id,
        "p_created_by": payload.created_by,
        "p_profile_image": payload.profile_image,
        "p_skill_id": payload.skill_id,
        "p_experience_summary": payload.experience_summary,
        "p_experience_doc": payload.experience_doc,
        "p_government_id": payload.government_id
    }

    result = execute_create_user_function(db, params)

    if not result:
        raise HTTPException(status_code=500, detail="User creation failed")

    try:
        data = dict(result._mapping)
    except:
        try:
            data = dict(result)
        except:
            data = result

    return {
        "message": "User registered successfully",
        "data": data
    }
