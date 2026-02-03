
# # from fastapi import APIRouter, Depends, HTTPException, status
# # from sqlalchemy.orm import Session

# # from core.database import get_db
# # from schemas.user_schema import (
# #     RegisterUser,
# #     RegisterResponse,
# #     LoginRequest,
# #     LoginResponse,
# #     VerifyTokenRequest,
# #     VerifyTokenResponse,
# #     RefreshRequest
# # )
# # from services.user_registration_service import (register_user,login_user)
# # from utils.jwt_utils import verify_token, create_access_token
# # from models.generated_models import UserRegistration

# # router = APIRouter(prefix="/api/auth",tags=["User Authentication"])

# # @router.post("/register",response_model=RegisterResponse,status_code=status.HTTP_201_CREATED)
# # def register(payload: RegisterUser,db: Session = Depends(get_db)):
# #     return register_user(db, payload)

# # @router.post("/login",response_model=LoginResponse)
# # def login(payload: LoginRequest,db: Session = Depends(get_db)):
# #     return login_user(db, payload)

# from fastapi import APIRouter, Depends, status
# from sqlalchemy.orm import Session

# from core.database import get_db

# from schemas.user_schema import (
#     RegisterUser,
#     RegisterUserResponse,
#     LoginRequest,
#     LoginResponse,
#     VerifyTokenRequest,
#     VerifyTokenResponse,
#     RefreshRequest
# )

# from services.user_registration_service import (
#     register_user,
#     login_user
# )

# from utils.jwt_utils import verify_token, create_access_token
# from models.generated_models import UserRegistration


# router = APIRouter(
#     prefix="/api/auth",
#     tags=["User Authentication"]
# )

# # -------------------------------------------------
# # Register
# # -------------------------------------------------
# @router.post(
#     "/register",
#     response_model=RegisterUserResponse,
#     status_code=status.HTTP_201_CREATED
# )
# def register(
#     payload: RegisterUser,
#     db: Session = Depends(get_db)
# ):
#     """
#     User registration API.
#     - Uses minimal UI fields
#     - Auto-login enabled
#     """
#     return register_user(db, payload)


# # -------------------------------------------------
# # Login
# # -------------------------------------------------
# @router.post(
#     "/login",
#     response_model=LoginResponse,
#     status_code=status.HTTP_200_OK
# )
# def login(
#     payload: LoginRequest,
#     db: Session = Depends(get_db)
# ):
#     """
#     Login using email or mobile.
#     Only APPROVED users allowed.
#     """
#     return login_user(db, payload)


# # -------------------------------------------------
# # Verify Access Token
# # -------------------------------------------------
# @router.post(
#     "/verify-token",
#     response_model=VerifyTokenResponse,
#     status_code=status.HTTP_200_OK
# )
# def verify_access_token(
#     payload: VerifyTokenRequest
# ):
#     """
#     Verify JWT access token validity.
#     """
#     data = verify_token(payload.token)

#     return VerifyTokenResponse(
#         authenticated=True,
#         token_type="bearer",
#         user_id=data.get("user_id"),
#         email=data.get("email"),
#         role_id=data.get("role_id"),
#         message="Token is valid"
#     )


# # -------------------------------------------------
# # Refresh Token
# # -------------------------------------------------
# @router.post(
#     "/refresh-token",
#     response_model=LoginResponse,
#     status_code=status.HTTP_200_OK
# )
# def refresh_token(
#     payload: RefreshRequest,
#     db: Session = Depends(get_db)
# ):
#     """
#     Issue new access token using refresh token.
#     """
#     user = (
#         db.query(UserRegistration)
#         .filter(UserRegistration.id == payload.user_id)
#         .first()
#     )

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
#         message="Token refreshed successfully",
#         user_id=user.id,
#         email_or_phone=user.email,
#         service_ids=[],
#         skill_ids=[],
#         access_token=create_access_token(token_payload),
#         refresh_token=payload.refresh_token,
#         expires_in=3600,
#         refresh_expires_in=86400,
#         role="refreshed"
#     )


from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.user_schema import (
    RegisterUser,
    RegisterResponse,
    LoginRequest,
    LoginResponse
)
from services.user_registration_service import register_user, login_user

router = APIRouter(
    prefix="/api/auth",
    tags=["User Authentication"]
)

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def register(payload: RegisterUser, db: Session = Depends(get_db)):
    return register_user(db, payload)


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, payload)
