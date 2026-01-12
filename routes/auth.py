import time
from datetime import datetime

import anyio
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer
from sqlalchemy import text
from sqlalchemy.orm import Session
from core.database import get_db
from services.user_controller import register_user_controller
from utils.mail_agent import send_welcome_email
from utils.sms_agent import send_welcome_sms
from utils.db_function import execute_function_raw
from utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from schemas.user_schema import RegisterUser, LoginRequest, LoginResponse, UpdateUser, VerifyTokenResponse
from passlib.context import CryptContext
import os

from fastapi import HTTPException, status
from pydantic import ValidationError

from schemas.user_schema import (ForgotPasswordRequest,VerifyOtpRequest,ResetPasswordRequest,)
from services import forgot_password_service as fp_service
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Response, Request
from core.database import get_db

router = APIRouter(prefix="/api/auth", tags=["Customer"])
security = HTTPBearer()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

async def hash_password(password: str) -> str:
    return await anyio.to_thread.run_sync(pwd_context.hash, password)

async def verify_password(plain: str, hashed: str) -> bool:
    return await anyio.to_thread.run_sync(pwd_context.verify, plain, hashed)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: RegisterUser,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = await register_user_controller(db, payload)


    background_tasks.add_task(
        send_welcome_sms,
        payload.mobile,
        payload.first_name
    )

    return {
        "message": "User registered successfully",
        "user_id": user["user_id"] if isinstance(user, dict) else user,
    }

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    identifier = payload.email_or_phone.strip()

    query = """
        SELECT * FROM fn_user_login_list(:p_identifier);
    """
    params = {"p_identifier": identifier}

    row = execute_function_raw(db, query, params)

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    user = dict(row._mapping) if hasattr(row, "_mapping") else dict(row)

    print("DB RESULT (login):", user)

    if not verify_password(payload.password, user.get("password", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    subject = {
        "user_id": user.get("user_id"),
        "email": user.get("email")
    }

    access_token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)

    refresh_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    refresh_max_age = refresh_days * 24 * 3600

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=refresh_max_age,
    )

    expires_in = int(os.getenv("JWT_EXPIRE_MINUTES", 15)) * 60

    return LoginResponse(
        id=user.get("user_id"),       
        email_or_phone=payload.email_or_phone,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=expires_in,
        refresh_expires_in=refresh_max_age
    )


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    query = text("SELECT * FROM user_registration ORDER BY id;")
    result = db.execute(query).fetchall()

    users = [dict(row._mapping) for row in result]

    return {
        "total_users": len(users),
        "users": users
    }


@router.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    query = text("SELECT * FROM user_registration WHERE id = :id LIMIT 1;")
    row = db.execute(query, {"id": user_id}).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    return {"user": dict(row._mapping)}


@router.put("/update")
def update_user(payload: UpdateUser, db: Session = Depends(get_db)):

    user_query = db.execute(text("SELECT * FROM user_registration WHERE id = :id"), {"id": payload.user_id})
    user = user_query.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = dict(user._mapping)
    updated_data = {
        "p_user_id": payload.user_id,
        "p_email": payload.email or user["email"],
        "p_first_name": payload.first_name or user["first_name"],
        "p_last_name": payload.last_name or user["last_name"],
        "p_mobile": payload.mobile or user["mobile"],
        "p_password": hash_password(payload.password) if payload.password else user["password"],
        "p_gender_id": payload.gender_id or user["gender_id"],
        "p_dob": user["dob"],
        "p_age": user["age"],
        "p_profile_image": user["profile_image"],
        "p_experience_summary": user["experience_summary"],
        "p_experience_doc": user["experience_doc"],
        "p_government_id": user["government_id"],
        "p_role_id": user["role_id"],
        "p_state_id": user["state_id"],
        "p_district_id": user["district_id"],
        "p_skill_id": user["skill_id"],
        "p_created_by": user["created_by"],

        "p_address": payload.address or user["address"]
    }

    query = """
    SELECT * FROM fn_user_update_list(
        :p_user_id,
        :p_email,
        :p_first_name,
        :p_last_name,
        :p_mobile,
        :p_password,
        :p_gender_id,
        :p_dob,
        :p_age,
        :p_profile_image,
        :p_experience_summary,
        :p_experience_doc,
        :p_government_id,
        :p_role_id,
        :p_state_id,
        :p_district_id,
        :p_skill_id,
        :p_created_by,
        :p_address
    );
    """

    result = db.execute(text(query), updated_data).fetchone()
    db.commit()

    return {"message": "User updated successfully", "updated": dict(result._mapping)}



@router.delete("/delete/{user_id}")
def delete_user_controller(user_id: int, db: Session = Depends(get_db)):
    query = "SELECT * FROM fn_user_delete_list(:p_user_id)"
    params = {"p_user_id": user_id}

    result = execute_function_raw(db, query, params)

    if not result:
        raise HTTPException(status_code=404, detail="Delete failed or user not found")

    return {"message": f"User {user_id} deleted successfully"}



@router.post("/forgot-password/request-otp")
async def forgot_password_request(
    body: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    try:
        await fp_service.request_password_reset(body.email, db)
    except fp_service.UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not registered",
        )

    return {"message": "OTP sent to registered email"}


@router.post("/forgot-password/verify-otp")
def forgot_password_verify(
    body: VerifyOtpRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        reset_token = fp_service.verify_otp(body.otp, db)
    except fp_service.OtpExpired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP expired, please request again",
        )
    except fp_service.InvalidOtp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP",
        )
    except fp_service.UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    max_age = 15 * 60 
    response.set_cookie(
        key="reset_token",
        value=reset_token,
        httponly=True,
        samesite="lax",
        max_age=max_age,
    )

    return {"message": "OTP verified successfully"}


@router.post("/forgot-password/reset")
def forgot_password_reset(
    body: ResetPasswordRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    if body.new_password != body.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    reset_token = request.cookies.get("reset_token")
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Reset token missing or expired. Please verify OTP again.",
        )

    try:
        fp_service.reset_password(reset_token, body.new_password, db)
    except fp_service.InvalidOtp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token. Please verify OTP again.",
        )
    except fp_service.UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    response.delete_cookie("reset_token")

    return {"message": "Password updated successfully"}
