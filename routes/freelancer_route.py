from fastapi import APIRouter, BackgroundTasks, Depends, Response,status
from sqlalchemy.orm import Session
from core.database import get_db
from utils.sms_agent import send_welcome_sms
from utils.jwt_utils import create_access_token
from schemas.user_schema import RefreshRequest, VerifyTokenResponse
from utils.jwt_utils import verify_token
from schemas.freelancer_schema import FreelancerRegister, FreelancerLogin,FreelancerUpdate,FreelancerResponse
from services.freelancer_service import (
   
    freelancer_register_service,
    freelancer_login_service,
    freelancer_update_service,
    freelancer_deactivate_service,
    freelancer_status_service,
    get_freelancer_by_id
)
from dependencies.auth_freelancer import get_current_freelancer


router = APIRouter(prefix="/api/freelancer", tags=["Freelancer"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_freelancer(
    payload: FreelancerRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    
    response = freelancer_register_service(db, payload)

    background_tasks.add_task(
        send_welcome_sms,
        payload.mobile,
        payload.first_name
    )

    return response

@router.get("/status/{freelancer_id}")
def get_freelancer_status(
    freelancer_id: int,
    db: Session = Depends(get_db)
):
  return freelancer_status_service(db, freelancer_id)

@router.post("/login")
def login_freelancer(payload: FreelancerLogin, response: Response, db: Session = Depends(get_db)):
    return freelancer_login_service(db, payload, response)

@router.get("/me")
def get_freelancer_profile(
    current_freelancer=Depends(get_current_freelancer),
    db=Depends(get_db)
):
   return get_freelancer_by_id(
        db=db,
        freelancer_id=current_freelancer.id
    )

@router.put("/update/{freelancer_id}")
def update_freelancer(
    payload: FreelancerUpdate,
    db: Session = Depends(get_db),
    current_freelancer=Depends(get_current_freelancer)
):
  return freelancer_update_service(
        db=db,
        freelancer_id=current_freelancer.id,
        payload=payload
  )

@router.delete("/deactivate/{freelancer_id}")
def deactivate_freelancer(
    db: Session = Depends(get_db),
    current_freelancer=Depends(get_current_freelancer)
):
    return freelancer_deactivate_service(db, current_freelancer.id)


