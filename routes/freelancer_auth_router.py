from fastapi import APIRouter, BackgroundTasks, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.freelancer_schema import FreelancerRegister, FreelancerLogin, FreelancerLogout
from schemas.user_schema import RefreshRequest
from services.freelancer_service import (
    freelancer_register_service,
    freelancer_login_service
)
from utils.sms_agent import send_welcome_sms
from utils.jwt_utils import verify_token, create_access_token

router = APIRouter(
    prefix="/api/freelancer",
    tags=["Freelancer Auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Register Freelancer")
async def register_freelancer(
    payload: FreelancerRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = freelancer_register_service(db, payload)

    background_tasks.add_task(
        send_welcome_sms,
        payload.mobile,
        payload.first_name
    )

    return {
        "message": "Freelancer registered successfully",
        "user_id": user["user_id"]
    }


@router.post("/login", summary="Login Freelancer")
def login_freelancer(
    payload: FreelancerLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    return freelancer_login_service(db, payload, response)


@router.post("/logout", summary="Logout Freelancer")
def logout_freelancer(response: Response):
    response.delete_cookie(
        key="freelancer_refresh_token",
        samesite="lax"
    )
    return {"message": "Freelancer logged out successfully"}


@router.post("/refresh", summary="Refresh Access Token")
def refresh_access_token(payload: RefreshRequest):
    decoded = verify_token(payload.refresh_token)

    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token({
        "user_id": decoded.get("sub"),
        "email": decoded.get("email"),
        "role": decoded.get("role")
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
