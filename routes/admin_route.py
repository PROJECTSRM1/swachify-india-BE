from fastapi import APIRouter, Depends, Request, Response, Header, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.constants import ADMIN_ROLE_ID, CUSTOMER_ROLE_ID, FREELANCER_ROLE_ID
from schemas.admin_schema import (
    RegisterAdmin, UserBase, AdminLogin, AdminLogout,
    AdminRegisterResponse, AdminUpdateResponse
)
from services.admin_service import (
    register_admin_service, admin_login_service, admin_update_service,
    admin_delete_service, admin_hard_delete_service, get_pending_freelancers_service,
    approve_freelancer_service, reject_freelancer_service,
    get_all_customers_service, get_customer_details_service
)
from utils.jwt_utils import verify_admin_token, verify_token
from models.user_registration import UserRegistration
import json
from models.master.master_gender import MasterGender
from models.master.master_skill import MasterSkill
from models.master.master_state import MasterState
from models.master.master_district import MasterDistrict

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.post("/register", response_model=AdminRegisterResponse)
def register_admin(request: RegisterAdmin, db: Session = Depends(get_db)):
    return register_admin_service(request, db)

@router.post("/login")
def admin_login(request: AdminLogin, db: Session = Depends(get_db), req: Request = None):
    """Admin login endpoint. Returns JWT tokens and admin info."""
    return admin_login_service(request, db, req)

@router.get("/admin/profile")
def get_admin_profile(payload = Depends(verify_admin_token)):
    return {"message": "Authorized", "admin": payload}


@router.put("/update/{admin_id}", response_model=AdminUpdateResponse)
def update_admin(admin_id: int, payload: dict, db: Session = Depends(get_db)):
    return admin_update_service(db, admin_id, payload)

@router.delete("/delete/{admin_id}")
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    return admin_delete_service(db, admin_id)

@router.delete("/hard-delete/{admin_id}")
def hard_delete_admin(admin_id: int, db: Session = Depends(get_db)):
    return admin_hard_delete_service(db, admin_id)

def get_current_admin(token: str) -> dict:
    """
    Verify admin JWT token and validate admin role.
    
    Args:
        token: JWT token from Authorization header
    
    Returns:
        Token payload dictionary with user_id, email, role_id
    
    Raises:
        HTTPException: If token invalid or user is not admin
    """
    payload = verify_token(token)
    
    # Check if user has admin role (role_id = 1)
    if payload.get("role_id") != ADMIN_ROLE_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return payload

@router.get("/pending")
def get_pending_freelancers(token: str, db: Session = Depends(get_db)):
    """Fetch all freelancers with PENDING approval status."""
    admin = get_current_admin(token)
    return get_pending_freelancers_service(db)


@router.put("/{freelancer_id}/approve")
def approve_freelancer(freelancer_id: int, token: str, db: Session = Depends(get_db)):
    """Approve a PENDING freelancer (status: PENDING → APPROVED)."""
    admin = get_current_admin(token)
    admin_id = int(admin["user_id"])  # Extract from JWT token
    return approve_freelancer_service(db, freelancer_id, admin_id)


@router.put("/{freelancer_id}/reject")
def reject_freelancer(freelancer_id: int, token: str, db: Session = Depends(get_db)):
    """Reject a PENDING freelancer (status: PENDING → REJECTED)."""
    admin = get_current_admin(token)
    admin_id = int(admin["user_id"])  # Extract from JWT token
    return reject_freelancer_service(db, freelancer_id, admin_id)


@router.get("/freelancer/{freelancer_id}")
def get_freelancer_full_details(freelancer_id: int, db: Session = Depends(get_db)):
    """
    Fetch complete freelancer profile details including skills, location, and documents.
    Masks sensitive government ID numbers for privacy.
    """
    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID
    ).first()

    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer not found")

    state_name = db.query(MasterState.state_name).filter(
        MasterState.id == freelancer.state_id
    ).scalar() if freelancer.state_id else None
    
    district_name = db.query(MasterDistrict.district_name).filter(
        MasterDistrict.id == freelancer.district_id
    ).scalar() if freelancer.district_id else None
    
    # Get skills from the relationship (UserSkill junction table)
    skills_list = []
    if freelancer.skills:
        for user_skill in freelancer.skills:
            skill_name = db.query(MasterSkill.skill).filter(
                MasterSkill.id == user_skill.skill_id
            ).scalar()
            if skill_name:
                skills_list.append(skill_name)
    
    skill_name = ", ".join(skills_list) if skills_list else None
    
    gender_value = db.query(MasterGender.gender_name).filter(
        MasterGender.id == freelancer.gender_id
    ).scalar() if freelancer.gender_id else None

    government_type = None
    government_number = None

    if freelancer.government_id:
        try:
            gov_data = json.loads(freelancer.government_id)
            government_type = gov_data.get("type")
            number = gov_data.get("number")

            if number:
                if len(number) > 4:
                    government_number = number[:2] + "*" * (len(number) - 4) + number[-2:]
                else:
                    government_number = "****"
        except:
            government_type = None
            government_number = None

    response = {
        "user_id": freelancer.id,
        "full_name": f"{freelancer.first_name} {freelancer.last_name or ''}".strip(),
        "mobile": freelancer.mobile,
        "email": freelancer.email,
        "gender": gender_value,
        "state": state_name,
        "district": district_name,
        "skill_name": skill_name,
        "government_id_type": government_type,
        "government_id_number": government_number,
        "address": freelancer.address,
        "rating": None,
        "completed_jobs": None,
        "status": "active" if freelancer.is_active else "inactive"
    }

    return {
        "status": "success",
        "code": 200,
        "message": "Freelancer details fetched successfully",
        "data": response
    }


@router.get("/freelancers")
def get_freelancer_list(db: Session = Depends(get_db)):
    """Fetch all active freelancers."""
    freelancers = db.query(UserRegistration).filter(
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active == True
    ).all()

    return freelancers


@router.get("/customers")
def get_all_customers(db: Session = Depends(get_db)):
    """
    Fetch all active customers.
    
    Returns:
        List of all active customer records
    """
    return get_all_customers_service(db)


@router.get("/customer/{customer_id}")
def get_customer_full_details(customer_id: int, db: Session = Depends(get_db)):
    """
    Fetch complete customer profile details including location and contact information.
    
    Args:
        customer_id: Customer user ID
        db: Database session
    
    Returns:
        Dictionary with customer details including name, contact, location, and account status
    """
    return get_customer_details_service(db, customer_id)