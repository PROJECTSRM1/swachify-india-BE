from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer
from sqlalchemy import text
from sqlalchemy.orm import Session
from core.database import get_db
from controllers.user_controller import register_user_controller
from utils.db_function import execute_create_user_function, execute_function_raw
from utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from schemas.user_schema import LogoutRequest, RegisterUser, LoginRequest, LoginResponse, UpdateUser, VerifyTokenResponse
from passlib.context import CryptContext
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])


security = HTTPBearer()

# -----------------------------------------
# PASSWORD HASH & VERIFY
# -----------------------------------------
pwd_context = CryptContext(
    schemes=["sha256_crypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


# -----------------------------------------
# REGISTER USER
# -----------------------------------------
@router.post("/register", status_code=201)
def register_user(payload: RegisterUser, db: Session = Depends(get_db)):
    return register_user_controller(db, payload)



@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    identifier = payload.email_or_phone.strip()

    # call DB function that returns user row (must return user_id/email/password ...)
    query = "SELECT * FROM fn_user_login_list(:p_email);"
    params = {"p_email": identifier}

    row = execute_function_raw(db, query, params)

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    # If execute_function_raw returns a Row, convert to mapping safely
    # Some DB layers return Row with _mapping, others already a dict.
    if hasattr(row, "_mapping"):
        user = dict(row._mapping)
    elif isinstance(row, dict):
        user = row
    else:
        # fallback: try to coerce to dict
        try:
            user = dict(row)
        except Exception:
            raise HTTPException(status_code=500, detail="Unexpected DB result format")

    # debug print (optional, remove in production)
    print("DB RESULT (login):", user)

    # verify password: plain -> payload.password, hashed -> user['password']
    if not verify_password(payload.password, user.get("password", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # IMPORTANT: create_access_token expects 'user_id' key in subject in your jwt_utils
    subject = {
        "user_id": user.get("user_id"),   # <-- match jwt_utils expectation
        "email": user.get("email")
    }

    access_token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)

    # cookie expiry
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

    # Optional DB check
    query = text("SELECT id FROM user_registration WHERE id = :id LIMIT 1;")
    result = db.execute(query, {"id": user_id}).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete refresh cookie
    response.delete_cookie("refresh_token")

    return {"message": f"User {user_id} logged out successfully"}

@router.get("/verify-token", response_model=VerifyTokenResponse)
def verify_token_endpoint(token: str):
    payload = verify_token(token)

    token_type = payload.get("type")

    if token_type == "access":
        message = "Valid access token"
    elif token_type == "refresh":
        message = "Valid refresh token"
    else:
        message = "Valid token"

    return VerifyTokenResponse(
        authenticated=True,
        token_type=token_type,
        user_id=payload.get("sub"),
        email=payload.get("email"),
        message=message
    )


@router.get("/me")
def get_current_user(token: str):
    payload = verify_token(token)

    return {
        "message": "Authenticated user",
        "user": payload
    }


@router.put("/update/{user_id}")
def update_user(user_id: int, payload: UpdateUser, db: Session = Depends(get_db)):

    # Prepare params for function
    params = {
        "p_user_id": user_id,  # if your function requires ID — LIST THIS IF NEEDED
        "p_email": payload.email,
        "p_first_name": payload.first_name,
        "p_last_name": payload.last_name,
        "p_mobile": payload.mobile,
        "p_password": hash_password(payload.password) if payload.password else None,
        "p_dob": payload.dob,
        "p_age": payload.age,
        "p_profile_image": payload.profile_image,
        "p_experience_summary": payload.experience_summary,
        "p_experience_doc": payload.experience_doc,
        "p_government_id": payload.government_id,
        "p_gender_id": payload.gender_id,
        "p_role_id": payload.role_id,
        "p_state_id": payload.state_id,
        "p_district_id": payload.district_id,
        "p_skill_id": payload.skill_id
    }

    # Clean: remove None values (function will break on NULL if not allowed)
    params = {k: v for k, v in params.items() if v is not None}

    # Call DB function
    query = """
        SELECT * FROM fn_user_update_list(
            :p_email,
            :p_first_name,
            :p_last_name,
            :p_mobile,
            :p_password,
            :p_dob,
            :p_age,
            :p_profile_image,
            :p_experience_summary,
            :p_experience_doc,
            :p_government_id,
            :p_gender_id,
            :p_role_id,
            :p_state_id,
            :p_district_id,
            :p_skill_id
        );
    """

    result = db.execute(text(query), params).fetchone()
    db.commit()

    if not result:
        raise HTTPException(status_code=404, detail="Update failed")

    return {
        "message": "User updated successfully",
        "updated_user": dict(result._mapping)
    }


# -----------------------------------------
# DELETE USER
# -----------------------------------------
@router.delete("/delete")
def delete_user_controller(email: str, db: Session = Depends(get_db)):
    query = "SELECT * FROM fn_user_delete_list(:p_email)"
    params = {"p_email": email}

    result = execute_function_raw(db, query, params)

    if not result:
        raise HTTPException(status_code=404, detail="Delete failed")

    return {"message": f"User {email} deleted successfully"}
