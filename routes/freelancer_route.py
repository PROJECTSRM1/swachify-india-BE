from datetime import datetime
import time
from fastapi import APIRouter, BackgroundTasks, Depends, Query, Response, HTTPException,status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from core.database import get_db
# from utils.mail_agent import send_welcome_email
from utils.sms_agent import send_welcome_sms
from utils.jwt_utils import create_access_token
from schemas.user_schema import RefreshRequest, VerifyTokenResponse
from utils.jwt_utils import verify_token
from schemas.freelancer_schema import FreelancerLogout, FreelancerRegister, FreelancerLogin
from services.freelancer_service import (
    fetch_customers_by_payment_status,
    # freelancer_paid_customers_service,
    freelancer_register_service,
    freelancer_login_service,
    freelancer_update_service,
    freelancer_delete_service,
    freelancer_status_service
)


router = APIRouter(prefix="/api/freelancer", tags=["Freelancer"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_freelancer(
    payload: FreelancerRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    user = freelancer_register_service(db, payload)

    # background_tasks.add_task(
    #     send_welcome_email,
    #     payload.email,
    #     payload.first_name
    # )


    background_tasks.add_task(
        send_welcome_sms,
        payload.mobile,
        payload.first_name
    )

    return {
        "message": "Freelancer registered successfully",
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



# @router.get("/{freelancer_id}/paid-services")
# def get_paid_customers_for_freelancer(
#     freelancer_id: int,
#     db: Session = Depends(get_db)
# ):
#     return freelancer_paid_customers_service(db, freelancer_id)


@router.get("/services")
def get_services_by_payment_status(
    payment_done: bool = Query(..., description="true = paid, false = unpaid"),
    db: Session = Depends(get_db)
):
    return fetch_customers_by_payment_status(db, payment_done)
