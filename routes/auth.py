# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status, Cookie
from sqlalchemy.orm import Session
from datetime import datetime
from core.database import get_db
from models.user_models import UserRegistration
from utils.hash import verify_password, hash_password
from utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from schemas.user_schema import RegisterUser, LoginRequest, LoginResponse,UpdateUser,VerifyTokenRequest,VerifyTokenResponse
import os
import json
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", status_code=201)
def register_user(payload: RegisterUser, db: Session = Depends(get_db)):

    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    exists = db.query(UserRegistration).filter(
        (UserRegistration.email == payload.email)
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


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):

    identifier = payload.email_or_phone.strip()

    user = db.query(UserRegistration).filter(
        UserRegistration.email == identifier
    ).first()

    if not user:
        user = db.query(UserRegistration).filter(
            UserRegistration.mobile == identifier
        ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    subject = {"user_id": user.id, "email": user.email}

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
        email_or_phone=payload.email_or_phone,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=expires_in,
        refresh_expires_in=refresh_max_age
    )


@router.post("/verify-token", response_model=VerifyTokenResponse)
async def verify_any_token(data: VerifyTokenRequest, db: Session = Depends(get_db)):

    token = data.token

    try:
        payload = verify_token(token)
        return VerifyTokenResponse(
            authenticated=False,
            message="Token expired"
        )
    except JWTError:
        return VerifyTokenResponse(
            authenticated=False,
            message="Invalid token"
        )

    # Extract data from token
    token_type = payload.get("type")
    sub = payload.get("sub")

    if not sub:
        return VerifyTokenResponse(
            authenticated=False,
            message="Invalid token payload"
        )

    user_id = sub.get("user_id")

    # Check if user actually exists
    user = db.query(UserRegistration).filter(UserRegistration.id == user_id).first()
    if not user:
        return VerifyTokenResponse(
            authenticated=False,
            message="User does not exist"
        )

    # SUCCESS
    return VerifyTokenResponse(
        authenticated=True,
        token_type=token_type,
        user_id=user.id,
        email=user.email,
        message="Token is valid"
    )


@router.post("/logout/{user_id}")
def logout(user_id: int, response: Response, db: Session = Depends(get_db)):

    user = db.query(UserRegistration).filter(UserRegistration.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    response.delete_cookie("refresh_token")

    return {"message": f"User {user_id} logged out successfully"}




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

    return {"message": "User updated successfully", "user": {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.mobile,
        "gender_id": user.gender_id
    }}



@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(UserRegistration).filter(UserRegistration.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": f"User {user_id} deleted successfully"}
