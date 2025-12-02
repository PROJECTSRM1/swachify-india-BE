from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from core.database import get_db
from controllers.user_controller import register_user_controller
from utils.db_function import execute_create_user_function, execute_function_raw
from utils.hash import verify_password, hash_password
from utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from schemas.user_schema import (
    RegisterUser, LoginRequest, LoginResponse,
    UpdateUser, VerifyTokenRequest, VerifyTokenResponse
)
import os
from jose import JWTError, ExpiredSignatureError

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register_user(payload: RegisterUser, db: Session = Depends(get_db)):
    return register_user_controller(db, payload)



@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):

    identifier = payload.email_or_phone.strip()

    query = """
        SELECT * FROM fn_login_user(:p_identifier);
    """
    params = {"p_identifier": identifier}

    result = execute_function_raw(db, query, params)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert Row to dict
    user = dict(result._mapping)

    # Validate password
    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # JWT subject
    subject = {
        "sub": user["user_id"],
        "email": user["email"]
    }

    access_token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)

    # Cookie expiry
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
        email_or_phone=payload.email_or_phone,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=expires_in,
        refresh_expires_in=refresh_max_age
    )


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}


@router.put("/update/{user_id}")
def update_user(user_id: int, payload: UpdateUser, db: Session = Depends(get_db)):

    # 1. Build dynamic SQL SET clause
    updates = {}
    if payload.full_name:
        updates["full_name"] = payload.full_name
    if payload.phone:
        updates["mobile"] = payload.phone
    if payload.gender_id:
        updates["gender_id"] = payload.gender_id
    if payload.password:
        updates["password"] = hash_password(payload.password)

    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    set_clause = ", ".join([f"{key} = :{key}" for key in updates.keys()])
    updates["id"] = user_id

    # 2. Execute dynamically generated update SQL
    query = text(f"""
        UPDATE user_registration
        SET {set_clause}
        WHERE id = :id
        RETURNING id, first_name, last_name, email, mobile, gender_id;
    """)

    result = db.execute(query, updates).fetchone()
    db.commit()

    if not result:
        raise HTTPException(status_code=404, detail="User not found or update failed")

    updated_user = dict(result._mapping)

    return {"message": "User updated successfully", "user": updated_user}



@router.delete("/delete/{user_id}")
def delete_user_controller(user_id: int, db: Session = Depends(get_db)):
    query = text("SELECT * FROM fn_delete_user_list(:p_user_id);")
    params = {"p_user_id": user_id}

    result = execute_function_raw(db, query, params)

    if not result:
        raise HTTPException(status_code=404, detail="User not found or delete failed")

    return {"message": f"User {user_id} deleted successfully"}
