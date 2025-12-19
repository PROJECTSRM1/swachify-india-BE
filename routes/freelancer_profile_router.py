from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from services.freelancer_service import freelancer_update_service,freelancer_deactivate_service
from dependencies.auth_dependency import get_current_freelancer
from schemas.freelancer_schema import FreelancerRegister

router = APIRouter(
    prefix="/api/freelancer",
    tags=["Freelancer Profile"]
)

@router.get("/me", summary="Get Current Freelancer Profile")
def get_current_freelancer_profile(
    current_user=Depends(get_current_freelancer)
):
    return current_user


@router.put("/me", summary="Update Freelancer Profile")
def update_current_freelancer(
    payload: FreelancerRegister,
    current_user=Depends(get_current_freelancer),
    db: Session = Depends(get_db)
):
    return freelancer_update_service(db, current_user.id, payload)


@router.delete("/me/deactivate", summary="Deactivate Freelancer Account")
def deactivate_current_freelancer(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_freelancer)
):
    return freelancer_deactivate_service(db, current_user)


