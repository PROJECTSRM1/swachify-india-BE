import os
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from controllers.user_controller import register_user_controller
from utils.sms_agent import send_welcome_sms
from utils.jwt_utils import create_access_token, create_refresh_token

CUSTOMER_ROLE_ID = int(os.getenv("CUSTOMER_ROLE_ID", "2"))
STATUS_APPROVED = int(os.getenv("STATUS_APPROVED", "1"))

async def register_user_service(
    db: Session,
    payload,
    background_tasks: BackgroundTasks
)-> dict:
    """
    Handles:
    - DB registration
    - Background notifications
    """

    payload.role_id = CUSTOMER_ROLE_ID
    payload.status_id = STATUS_APPROVED

    # 1️⃣ Register user (DB only)
    user = await register_user_controller(db, payload)

    if not user:
        raise HTTPException(
            status_code=500,
            detail="User registration failed"
        )
    
    subject={
        "user_id": str(user.id),
        "email": user.email,
        "role_id": "customer",
        "status": "approved"
    }

    access_token= create_access_token(subject)
    refresh_token= create_refresh_token(subject)

    # 2️⃣ Background SMS (non-blocking)
    background_tasks.add_task(
        send_welcome_sms,
        payload.mobile,
        payload.first_name
    )

    return {
         "message": "Customer registered successfully",
        "user_id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": int(os.getenv("JWT_EXPIRE_MINUTES", 15)) * 60
    }
