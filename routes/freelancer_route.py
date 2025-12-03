from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.freelancer_schema import FreelancerRegister, FreelancerLogin
from services.freelancer_service import freelancer_register_service, freelancer_login_service

router = APIRouter(prefix="/freelancer", tags=["Freelancer"])


@router.post("/register")
def register_freelancer(payload: FreelancerRegister, db: Session = Depends(get_db)):
    return freelancer_register_service(db, payload)


@router.post("/login")
def login_freelancer(payload: FreelancerLogin, response: Response, db: Session = Depends(get_db)):
    result = freelancer_login_service(db, payload)
    
    

    return result
