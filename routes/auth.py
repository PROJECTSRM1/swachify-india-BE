import time
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer
from sqlalchemy import text
from sqlalchemy.orm import Session
from core.database import get_db
from controllers.user_controller import register_user_controller
from utils.db_function import execute_create_user_function, execute_function_raw
from utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from schemas.user_schema import LogoutRequest, RefreshRequest, RegisterUser, LoginRequest, LoginResponse, UpdateUser, VerifyTokenResponse
from passlib.context import CryptContext
import os

from fastapi import HTTPException, status
from pydantic import ValidationError

router = APIRouter(prefix="/api/auth", tags=["auth"])


security = HTTPBearer()

pwd_context = CryptContext(
    schemes=["sha256_crypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterUser, db: Session = Depends(get_db)):
    try:
        payload = RegisterUser(**payload.dict())

    except ValidationError as e:
        error = e.errors()[0]["msg"]

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error
        )

    existing = db.execute(
        text("SELECT 1 FROM user_registration WHERE email=:email"),
        {"email": payload.email}
    ).fetchone()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    return register_user_controller(db, payload)

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    identifier = payload.email_or_phone.strip()

    query = """
        SELECT * FROM fn_user_login_list(:p_identifier);
    """

    params = {
        "p_identifier": identifier
    }

    row = execute_function_raw(db, query, params)

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    if hasattr(row, "_mapping"):
        user = dict(row._mapping)
    else:
        try:
            user = dict(row)
        except Exception:
            raise HTTPException(status_code=500, detail="Unexpected DB result format")

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
        email_or_phone=payload.email_or_phone,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=expires_in,
        refresh_expires_in=refresh_max_age
    )


@router.post("/logout")
def logout(payload: LogoutRequest, response: Response, db: Session = Depends(get_db)):

    user_id = payload.user_id

    query = text("SELECT id FROM user_registration WHERE id = :id LIMIT 1;")
    result = db.execute(query, {"id": user_id}).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    response.delete_cookie("refresh_token")

    return {"message": f"User {user_id} logged out successfully"}

@router.get("/verify-token", response_model=VerifyTokenResponse)
def verify_token_endpoint(token: str):
    payload = verify_token(token)

    token_type = payload.get("type") 

    return VerifyTokenResponse(
        authenticated=True,
        token_type=token_type,
        user_id=payload.get("sub"),
        email=payload.get("email"),
        message=f"Valid {token_type} token"
    )


@router.get("/me")
def get_current_user(token: str):
    print("PYTHON UTC NOW:", datetime.utcnow())
    print("PYTHON TIMESTAMP:", int(time.time()))

    payload = verify_token(token)
    return {"user": payload}




@router.put("/update")
def update_user(payload: UpdateUser, db: Session = Depends(get_db)):

    params = {
        "p_email": payload.email,
        "p_first_name": payload.first_name,
        "p_last_name": payload.last_name,
        "p_mobile": payload.mobile,
        "p_password": hash_password(payload.password) if payload.password else None,
        "p_gender_id": payload.gender_id,
        "p_dob": None,
        "p_age": None,
        "p_profile_image": None,
        "p_experience_summary": None,
        "p_experience_doc": None,
        "p_government_id": None,
        "p_role_id": None,
        "p_state_id": None,
        "p_district_id": None,
        "p_skill_id": None,
        "p_created_by": None,
        "p_address": payload.address
    }

    query = """
    SELECT * FROM fn_user_update_list(
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

    result = db.execute(text(query), params).fetchone()
    db.commit()

    if not result:
        raise HTTPException(status_code=404, detail="Update failed")

    return {
        "message": "User updated successfully",
        "updated": result._mapping
    }



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


@router.delete("/delete")
def delete_user_controller(email: str, db: Session = Depends(get_db)):
    query = "SELECT * FROM fn_user_delete_list(:p_email)"
    params = {"p_email": email}

    result = execute_function_raw(db, query, params)

    if not result:
        raise HTTPException(status_code=404, detail="Delete failed")

    return {"message": f"User {email} deleted successfully"}


@router.post("/refresh")
def refresh_access_token(payload: RefreshRequest):
    
    refresh_token = payload.refresh_token

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    decoded = verify_token(refresh_token)

    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({
        "user_id": decoded.get("sub"),
        "email": decoded.get("email")
    })

    return {
        "message": "New access token generated",
        "user_id": payload.user_id,
        "access_token": new_access_token,
        "token_type": "bearer"
    }
