from fastapi import APIRouter, Depends,Request,Response,Header,HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.admin_schema import RegisterAdmin, UserBase,AdminLogin,AdminLogout,AdminRegisterResponse,AdminUpdateResponse
from services.admin_service import register_admin_service,admin_login_service,admin_update_service,admin_delete_service,admin_hard_delete_service,get_pending_freelancers_service,approve_freelancer_service,reject_freelancer_service,assign_freelancer_to_home_service_service 
from services.home_service import get_home_services_by_creator_and_payment
from utils.jwt_utils import verify_admin_token,verify_token
from schemas.freelancer_details_schema import FreelancerDetailResponse,FreelancerSkill
from models.user_registration import UserRegistration
import json
from models.master.master_gender import MasterGender
from models.master.master_skill import MasterSkill
from models.master.master_state import MasterState
from models.master.master_district import MasterDistrict
from schemas.home_schema import HomeServiceFilter
from schemas.home_schema import AssignFreelancerRequest

router = APIRouter(prefix="/api/admin", tags=["Admin Authentication"])


@router.post("/register", response_model=AdminRegisterResponse)
def register_admin(request: RegisterAdmin, db: Session = Depends(get_db)):
    return register_admin_service(request, db)

@router.post("/login")   # no response_model to avoid strict validation issues
def admin_login(request: AdminLogin, db: Session = Depends(get_db),req: Request = None):
    return admin_login_service(request, db,req)

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

def get_current_admin(token: str):
    payload = verify_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload

@router.get("/pending")
def get_pending_freelancers(token: str,db: Session = Depends(get_db)):
    get_current_admin(token)
    return get_pending_freelancers_service(db)


@router.put("/{freelancer_id}/approve")
def approve_freelancer(freelancer_id: int,token: str,db: Session = Depends(get_db)):
    admin = get_current_admin(token)
    return approve_freelancer_service(db, freelancer_id, int(admin["sub"]))


@router.put("/{freelancer_id}/reject")
def reject_freelancer(freelancer_id: int,token: str,db: Session = Depends(get_db)):
    admin = get_current_admin(token)
    return reject_freelancer_service(db, freelancer_id, int(admin["sub"]))


@router.get("/freelancer/{freelancer_id}")
def get_freelancer_full_details(freelancer_id: int, db: Session = Depends(get_db)):
    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == 4 
    ).first()

    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer not found")

    state_name = db.query(MasterState.state_name).filter(MasterState.id == freelancer.state_id).scalar() if freelancer.state_id else None
    district_name = db.query(MasterDistrict.district_name).filter(MasterDistrict.id == freelancer.district_id).scalar() if freelancer.district_id else None
    skill_name = db.query(MasterSkill.skill).filter(MasterSkill.id == freelancer.skill_id).scalar() if freelancer.skill_id else None
    gender_value = db.query(MasterGender.gender_name).filter(MasterGender.id == freelancer.gender_id).scalar() if freelancer.gender_id else None

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
    freelancers = db.query(UserRegistration).filter(
        UserRegistration.role_id == 4,
        UserRegistration.is_active == True
    ).all()

    return freelancers

@router.post("/assign-freelancer")
def assign_freelancer_to_home_service(
    request: AssignFreelancerRequest,
    db: Session = Depends(get_db)
):
    return assign_freelancer_to_home_service_service(
        db=db,
        home_service_id=request.home_service_id,
        freelancer_id=request.freelancer_id
    )

@router.post("/by-user")
def get_home_services_by_user(
    filters: HomeServiceFilter,
    db: Session = Depends(get_db)
):
    return get_home_services_by_creator_and_payment(
        db=db,
        created_by=filters.created_by,
        payment_done=filters.payment_done
    )