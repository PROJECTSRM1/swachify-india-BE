from datetime import datetime
import time
from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from core.database import get_db
# from utils.mail_agent import send_welcome_email
# from utils.sms_agent import send_welcome_sms
from utils.jwt_utils import create_access_token
from schemas.user_schema import RefreshRequest, VerifyTokenResponse
from utils.jwt_utils import verify_token
from schemas.freelancer_schema import FreelancerLogout, FreelancerRegister, FreelancerLogin
from services.freelancer_service import (
    freelancer_register_service,
    freelancer_login_service,
    freelancer_update_service,
    freelancer_delete_service,
    freelancer_status_service
)


router = APIRouter(prefix="/api/freelancer", tags=["Freelancer"])

@router.post("/register")
async def register_freelancer(payload: FreelancerRegister, db: Session = Depends(get_db)):

    user = freelancer_register_service(db, payload)

    # # 2️⃣ Send Welcome Email
    # try:
    #     await send_welcome_email(
    #         email=payload.email,
    #         name=payload.first_name
    #     )
    # except Exception as e:
    #     print("EMAIL SEND ERROR:", e)

    # # 3️⃣ Send Welcome SMS
    # try:
    #     send_welcome_sms(
    #         mobile=payload.mobile,
    #         firstname=payload.first_name
    #     )
    # except Exception as e:
    #     print("SMS SEND ERROR:", e)

    return {
        "message": "Freelancer registered successfully. Notifications sent.",
        "user_id": user["user_id"] if isinstance(user, dict) else user
    }

@router.get("/status/{freelancer_id}")
def get_freelancer_status(
    freelancer_id: int,
    db: Session = Depends(get_db)
):
  return freelancer_status_service(db, freelancer_id)

@router.post("/login")
def login_freelancer(payload: FreelancerLogin, response: Response, db: Session = Depends(get_db)):
    return freelancer_login_service(db, payload, response)


@router.post("/logout")
def logout_freelancer(payload: FreelancerLogout, response: Response):
    
    # Clear refresh token cookie
    response.delete_cookie(
        key="freelancer_refresh_token",
        samesite="lax"
    )

    return {
        "message": "Freelancer logged out successfully",
        "user_id": payload.user_id
    }


# ============================
# CURRENT USER (ME)
# ============================
@router.get("/me")
def get_current_freelancer(token: str):
    """
    Access token must be passed as query param:
    /me?token=ACCESS_TOKEN
    """
    payload = verify_token(token)

    if payload.get("role") != "freelancer":
        raise HTTPException(status_code=403, detail="Unauthorized role")

    return {
        "authenticated": True,
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role")
    }




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


@router.put("/update/{freelancer_id}")
def update_freelancer(
    freelancer_id: int,
    payload: FreelancerRegister,
    db: Session = Depends(get_db)
):
    return freelancer_update_service(db, freelancer_id, payload)


@router.delete("/delete/{freelancer_id}")
def delete_freelancer(freelancer_id: int, db: Session = Depends(get_db)):
    return freelancer_delete_service(db, freelancer_id)
