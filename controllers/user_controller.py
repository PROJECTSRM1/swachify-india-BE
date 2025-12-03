from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.db_function import execute_create_user_function
from schemas.user_schema import RegisterUser
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["sha256_crypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


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
        "p_address": payload.address
    }

    result = execute_create_user_function(db, params)

    if not result:
        raise HTTPException(status_code=500, detail="User creation failed")

    return {
        "message": "User registered successfully",
        "data": dict(result._mapping)
    }
