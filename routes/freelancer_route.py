from datetime import datetime
import time
from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from core.database import get_db
# from utils.mail_agent import send_welcome_email
from utils.sms_agent import send_welcome_sms
# from utils.jwt_utils import create_access_token
from schemas.user_schema import RefreshRequest, VerifyTokenResponse
from utils.jwt_utils import verify_token
from utils.auth_dependencies import get_current_freelancer
from schemas.freelancer_schema import FreelancerRegister, FreelancerLogin
from services.freelancer_service import (
    freelancer_register_service,
    freelancer_login_service,
    freelancer_update_service,
    freelancer_delete_service,
    freelancer_status_service,
    get_freelancer_by_id,
    freelancer_complete_job_service,
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

    return user

@router.get("/status/{freelancer_id}")
def get_freelancer_status(
    freelancer_id: int,
    db: Session = Depends(get_db)
):
  return freelancer_status_service(db, freelancer_id)

@router.post("/login")
def login_freelancer(payload: FreelancerLogin, response: Response, db: Session = Depends(get_db)):
    return freelancer_login_service(db, payload, response)

@router.get("/{freelancer_id}")
def get_freelancer_details(
    freelancer_id: int,
    db: Session = Depends(get_db)
):
    return get_freelancer_by_id(db, freelancer_id)

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

@router.put("/services/{service_id}/complete", response_model=None)
def complete_service(
    service_id: int,
    db: Session = Depends(get_db),
    freelancer = Depends(get_current_freelancer)
):
    return freelancer_complete_job_service(
        db=db,
        freelancer_id=freelancer["user_id"],
        service_id=service_id
    )

