# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from datetime import datetime
from core.database import get_db
from models.user_models import UserRegistration
from utils.hash import verify_password, hash_password
from utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from schemas.user_schema import (
    RegisterUser, LoginRequest, LoginResponse,
    UpdateUser, VerifyTokenRequest, VerifyTokenResponse
)
import os
from jose import JWTError, ExpiredSignatureError

router = APIRouter(prefix="/api/auth", tags=["auth"])

# --------------------------------------------------
# REGISTER
# --------------------------------------------------
@router.post("/register", status_code=201)
def register_user(payload: RegisterUser, db: Session = Depends(get_db)):

    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    exists = db.query(UserRegistration).filter(
        UserRegistration.email == payload.email
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(payload.password)

    new_user = UserRegistration(
        full_name=payload.full_name,
        email=payload.email,
        mobile=payload.phone,
        password=hashed,
        gender_id=payload.gender_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered", "user_id": new_user.id}


# --------------------------------------------------
# LOGIN
# --------------------------------------------------
@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):

    identifier = payload.email_or_phone.strip()

    user = db.query(UserRegistration).filter(
        (UserRegistration.email == identifier) |
        (UserRegistration.mobile == identifier)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # subject → put user_id directly
    subject = {"sub": user.id, "email": user.email}

    access_token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)

    refresh_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    refresh_max_age = refresh_days * 24 * 3600

    # Store refresh token in cookie
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

@router.get("/me")
def get_current_user(user=Depends(verify_token)):
    return {
        "message": "Authenticated user",
        "user": user
    }


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------
@router.post("/logout/{user_id}")
def logout(user_id: int, response: Response, db: Session = Depends(get_db)):

    user = db.query(UserRegistration).filter(UserRegistration.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    response.delete_cookie("refresh_token")

    return {"message": f"User {user_id} logged out successfully"}


# --------------------------------------------------
# UPDATE USER
# --------------------------------------------------
@router.put("/update/{user_id}")
def update_user(user_id: int, payload: UpdateUser, db: Session = Depends(get_db)):

    user = db.query(UserRegistration).filter(UserRegistration.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.full_name:
        user.full_name = payload.full_name

    if payload.phone:
        user.mobile = payload.phone

    if payload.gender_id:
        user.gender_id = payload.gender_id

    if payload.password:
        user.password = hash_password(payload.password)

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.mobile,
            "gender_id": user.gender_id
        }
    }


# --------------------------------------------------
# DELETE USER
# --------------------------------------------------
@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(UserRegistration).filter(UserRegistration.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": f"User {user_id} deleted successfully"}
