from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.user_schema import (
    RegisterUser,
    RegisterResponse,
    LoginRequest,
    LoginResponse
)
from services.user_registration_service import (
    register_user,
    login_user
)

router = APIRouter(
    prefix="/api",
    tags=["User Auth"]
)


# ==================================================
# 🔹 REGISTER
# ==================================================
@router.post("/auth/register", response_model=RegisterResponse)
def register(payload: RegisterUser, db: Session = Depends(get_db)):
    user, message = register_user(db, payload)

    return RegisterResponse(
        message=message,
        user_id=user.id,
        unique_id=user.unique_id,
        email=user.email,
        mobile=user.mobile,
        role_id=user.role_id,
        status_id=user.status_id
    )


# ==================================================
# 🔹 LOGIN
# ==================================================
@router.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, payload)








