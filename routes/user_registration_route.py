
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.user_schema import (
    RegisterUser,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    VerifyTokenRequest,
    VerifyTokenResponse,
    RefreshRequest
)
from services.user_registration_service import (register_user,login_user)
from utils.jwt_utils import verify_token, create_access_token
# from models.user_registration import UserRegistration
from models.generated_models import UserRegistration

router = APIRouter(prefix="/api/auth",tags=["User Authentication"])

@router.post("/register",response_model=RegisterResponse,status_code=status.HTTP_201_CREATED)
def register(payload: RegisterUser,db: Session = Depends(get_db)):
    return register_user(db, payload)

@router.post("/login",response_model=LoginResponse)
def login(payload: LoginRequest,db: Session = Depends(get_db)):
    return login_user(db, payload)

