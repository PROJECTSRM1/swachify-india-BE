from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Request
from models.user_registration import UserRegistration
from models.home_service import HomeService

from schemas.admin_schema import RegisterAdmin,AdminLogin,AdminLogout,UserBase,AdminRegisterResponse
from utils.hash_utils import hash_password,verify_password
from utils.jwt_utils import create_access_token,create_refresh_token,is_admin_already_logged_in
import uuid
import os
from sqlalchemy import or_
from datetime import datetime

ADMIN_ROLE_ID = 1
FREELANCER_ROLE_ID = 4

STATUS_APPROVED = 1
STATUS_PENDING = 2
STATUS_REJECTED = 3

def register_admin_service(request: RegisterAdmin, db: Session):
    if db.query(UserRegistration).filter(UserRegistration.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    if db.query(UserRegistration).filter(UserRegistration.mobile == request.mobile).first():
        raise HTTPException(status_code=400, detail="Mobile number already exists")

    admin = UserRegistration(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        mobile=request.mobile,
        password=hash_password(request.password),
        gender_id=request.gender_id,
        address=request.address,
        role_id=1,
        is_active=True,
        unique_id = str(uuid.uuid4())
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return {
        "message": "Admin registered successfully",
        "data": admin
    }

def admin_login_service(credentials: AdminLogin, db: Session,http_request:Request):
    if is_admin_already_logged_in(http_request):
        return {
            "status": "warning",
            "code": 409,
            "message": "Admin already logged in. Please logout to login again."
        }

    identifier = credentials.username_or_email.strip()

    query = db.query(UserRegistration).filter(UserRegistration.role_id == 1)

    admin = query.filter(
        or_(
            UserRegistration.email == identifier,
            UserRegistration.mobile == identifier,
            UserRegistration.unique_id == identifier,
        )
    ).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(credentials.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    payload = {
    "sub": str(admin.id),
    "email": admin.email,
    "role": "admin"
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    user_data = UserBase.model_validate(admin)

    return {
        "message": "Login successful",
        "user": user_data,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }



def admin_update_service(db: Session, admin_id: int, payload: dict):
    admin = db.query(UserRegistration).filter(
        UserRegistration.id == admin_id,
        UserRegistration.role_id == 1 
    ).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    if "email" in payload and payload["email"] != admin.email:
        existing_email = db.query(UserRegistration).filter(
            UserRegistration.email == payload["email"],
            UserRegistration.id != admin_id  
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")

    if "mobile" in payload and payload["mobile"] != admin.mobile:
        existing_mobile = db.query(UserRegistration).filter(
            UserRegistration.mobile == payload["mobile"],
            UserRegistration.id != admin_id   
        ).first()
        if existing_mobile:
            raise HTTPException(status_code=400, detail="Mobile number already exists")

    for key, value in payload.items():
        setattr(admin, key, value)

    admin.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(admin)
    return {
        "message": "Admin details updated successfully",
        "data": admin
    }


def admin_delete_service(db: Session, admin_id: int):
    admin = db.query(UserRegistration).filter(
        UserRegistration.id == admin_id,
        UserRegistration.role_id == 1 
    ).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    admin.is_active = False
    admin.modified_date = datetime.utcnow()

    db.commit()
    return {"message": "Admin deactivated successfully"}

def admin_hard_delete_service(db: Session, admin_id: int):
    admin = db.query(UserRegistration).filter(
        UserRegistration.id == admin_id,
        UserRegistration.role_id == 1
    ).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    db.delete(admin)
    db.commit()
    return {"message": "Admin deleted permanently"}

def get_pending_freelancers_service(db: Session):
    return db.query(UserRegistration).filter(
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.status_id == STATUS_PENDING,
        UserRegistration.is_active == True
    ).all()


def approve_freelancer_service(db: Session, freelancer_id: int, admin_id: int):
    user = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID
    ).first()

    if not user:
        raise HTTPException(404, "Freelancer not found")

    user.status_id = STATUS_APPROVED
    user.modified_by = admin_id

    db.commit()
    db.refresh(user)

    return {
        "message": "Freelancer approved successfully",
        "freelancer_id": user.id,
        "status": "Approved"
    }


def reject_freelancer_service(db: Session, freelancer_id: int, admin_id: int):
    user = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID
    ).first()

    if not user:
        raise HTTPException(404, "Freelancer not found")

    user.status_id = STATUS_REJECTED
    user.modified_by = admin_id

    db.commit()
    db.refresh(user)

    return {
        "message": "Freelancer rejected",
        "freelancer_id": user.id,
        "status": "Rejected"
    }
    
def assign_freelancer_to_home_service_service(
    db: Session,
    home_service_id: int,
    freelancer_id: int
):
   
    home_service = db.query(HomeService).filter(
        HomeService.id == home_service_id
    ).first()

    if not home_service:
        raise HTTPException(status_code=404, detail="Home service not found")

   
    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active == True
    ).first()

    if not freelancer:
        raise HTTPException(status_code=404, detail="Freelancer not found")

    
    home_service.status_id = STATUS_PENDING
    home_service.assigned_to = freelancer_id

   
    freelancer.status_id = STATUS_PENDING

    db.commit()
    db.refresh(home_service)
    db.refresh(freelancer)

    return {
        "message": "Freelancer assigned to home service successfully",
        "home_service_id": home_service.id,
        "freelancer_id": freelancer.id
    }
