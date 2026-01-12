
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
from services.user_registration_service import (
    register_user,
    login_user
)
from utils.jwt_utils import verify_token, create_access_token
from models.user_registration import UserRegistration

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: RegisterUser,
    db: Session = Depends(get_db)
):
    """
    - Registers user
    - Issues access & refresh tokens immediately
    """
    return register_user(db, payload)


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    return login_user(db, payload)


# ==================================================
# 🔹 VERIFY TOKEN
# ==================================================
# @router.post(
#     "/verify-token",
#     response_model=VerifyTokenResponse
# )
# def verify_access_token(payload: VerifyTokenRequest):
#     """
#     Validates JWT and returns user info
#     """
#     try:
#         decoded = verify_token(payload.token)

#         return VerifyTokenResponse(
#             authenticated=True,
#             token_type=decoded.get("type"),
#             user_id=decoded.get("user_id"),
#             email=decoded.get("email"),
#             role_id=decoded.get("role_id"),
#             message="Token is valid"
#         )

#     except HTTPException as e:
#         return VerifyTokenResponse(
#             authenticated=False,
#             message=e.detail
#         )


# # ==================================================
# # 🔹 REFRESH TOKEN
# # ==================================================
# @router.post(
#     "/refresh-token",
#     response_model=LoginResponse
# )
# def refresh_access_token(
#     payload: RefreshRequest,
#     db: Session = Depends(get_db)
# ):
#     """
#     Issues a new access token using refresh token
#     """

#     decoded = verify_token(payload.refresh_token)

#     if decoded.get("type") != "refresh":
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid refresh token"
#         )

#     user = db.query(UserRegistration).filter(
#         UserRegistration.id == payload.user_id
#     ).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )

#     token_payload = {
#         "user_id": user.id,
#         "email": user.email,
#         "role_id": user.role_id
#     }

#     return LoginResponse(
#         user_id=user.id,
#         email_or_phone=user.email,
#         access_token=create_access_token(token_payload),
#         refresh_token=payload.refresh_token,
#         expires_in=60 * 60,
#         refresh_expires_in=60 * 60 * 24
#     )
