from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer

from core.database import get_db
from core.dependencies import get_current_user

# ---------------- SCHEMAS ----------------
from schemas.student_education_schema import (
    StudentCertificateCreate,
    StudentCertificateResponse,
    StudentProfileResponse,
    StudentEducationCreate,
    StudentNOCUpdate,
    StudentNOCResponse
)

# ---------------- SERVICES ----------------
from services.student_education_service import (
    create_student_certificate,
    add_student_education_service,
    update_student_noc
)

# ---------------- MODELS ----------------
from models.user_registration import UserRegistration
from models.master_module import MasterModule

# ---------------- ROUTER ----------------
router = APIRouter(
    prefix="/api/student",
    tags=["Education Module"]
)

bearer_scheme = HTTPBearer()

# ==================================================
# ADD CERTIFICATE
# ==================================================
@router.post(
    "/education/certifications",
    response_model=StudentCertificateResponse
)
def add_certificate(
    payload: StudentCertificateCreate,
    db: Session = Depends(get_db),
    current_user: UserRegistration = Depends(get_current_user)
):
    return create_student_certificate(
        db=db,
        payload=payload,
        user_id=current_user.id   # ✅ FIX
    )

# ==================================================
# UPDATE NOC
# ==================================================
@router.post(
    "/education/noc",
    response_model=StudentNOCResponse
)
def save_student_noc(
    payload: StudentNOCUpdate,
    db: Session = Depends(get_db),
    current_user: UserRegistration = Depends(get_current_user)
):
    user = update_student_noc(
        db=db,
        payload=payload,
        user_id=current_user.id   # ✅ SAFE
    )

    return {
        "user_id": user.id,
        "noc_number": user.noc_number,
        "police_station_name": user.police_station_name,
        "issue_year": user.issue_year,
        "upload_noc": user.upload_noc
    }

# ==================================================
# GET STUDENT PROFILE
# ==================================================
@router.get(
    "/education/profile",
    response_model=StudentProfileResponse,
    dependencies=[Security(bearer_scheme)]
)
def get_student_profile(
    current_user: UserRegistration = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == current_user.id,
            UserRegistration.services.any(
                MasterModule.module_name == "Education"
            )
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    # ✅ MAP RESPONSE EXPLICITLY
    return StudentProfileResponse(
        user_id=student.id,
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        mobile_number=student.mobile,
        government_id=student.government_id,
        location=student.address,
        service_name="Education"
    )

# ==================================================
# ADD EDUCATION DETAILS
# ==================================================
@router.post("/education")
def add_student_education(
    payload: StudentEducationCreate,
    db: Session = Depends(get_db),
    current_user: UserRegistration = Depends(get_current_user)
):
    education = add_student_education_service(
        user_id=current_user.id,
        payload=payload,
        db=db
    )

    return {
        "message": "Education qualification added successfully",
        "user_id": current_user.id,
        "education_id": education.id
    }
