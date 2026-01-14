from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from core.database import get_db
from core.dependencies import get_current_user

from schemas.student_education_schema import (
    StudentCertificateCreate,
    StudentCertificateResponse,
    StudentProfileResponse,
    StudentProfileRequest,
    StudentEducationCreate,
    StudentNOCUpdate,
    StudentNOCResponse
)

from services.student_education_service import (
    create_student_certificate,
    get_student_certificates,
    add_student_education_service,
    update_student_noc
)

from models.user_registration import UserRegistration
from models.master_module import MasterModule


router = APIRouter(prefix="/api/student/education", tags=["Student Education"])
bearer_scheme = HTTPBearer() 

# ================= CERTIFICATION =================

@router.post("/certifications")
def add_certificate(
    payload: StudentCertificateCreate,
    db: Session = Depends(get_db),
):
    return create_student_certificate(db, payload)


# @router.get("/certifications", response_model=list[StudentCertificateResponse])
# def fetch_certificates(
#     db: Session = Depends(get_db),
#     user_id: int = 1
# ):
#     return get_student_certificates(db, user_id)


# ================= NOC =================

@router.post("/noc", response_model=StudentNOCResponse)
def save_student_noc(
    payload: StudentNOCUpdate,
    db: Session = Depends(get_db)
):
    user = update_student_noc(db, payload)

    return {
        "user_id": user.id,
        "noc_number": user.noc_number,
        "police_station_name": user.police_station_name,
        "issue_year": user.issue_year,
        "upload_noc": user.upload_noc
    }


# ==================================================
# 🔹 GET PROFILE (LOGGED-IN USER)
# ==================================================

# @router.get("/profile", response_model=StudentProfileResponse)
# def get_student_profile(
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
    

#     student = (
#         db.query(UserRegistration)
#         .join(MasterModule, UserRegistration.services == MasterModule.id)
#         .filter(
#             UserRegistration.id == user_id,
#             MasterModule.module_name == "Education"
#         )
#         .first()
#     )

#     if not student:
#         raise HTTPException(
#             status_code=404,
#             detail="Student profile not found"
#         )

#     return StudentProfileResponse(
#         user_id=user_id,
#         first_name=student.first_name,
#         last_name=student.last_name,
#         email=student.email,
#         mobile_number=student.mobile_number,
#         aadhaar_number=student.aadhaar_number,
#         location=student.location,
#         work_type=student.work_type,
#         service_name=student.service.module_name
#     )
# @router.get(
#     "/profile",
#     response_model=StudentProfileResponse,
#     dependencies=[Security(bearer_scheme)]  # 👈 THIS LINE
# )

@router.get(
    "/profile",
    response_model=StudentProfileResponse,
    dependencies=[Security(bearer_scheme)]
)

def get_student_profile(
    current_user: UserRegistration = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    student = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == user_id,
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
# 🔹 POST EDUCATION (LOGGED-IN USER)
# ==================================================

@router.post("")
def add_student_education(
    payload: StudentEducationCreate,
    db: Session = Depends(get_db)
):
    

    education = add_student_education_service(
        user_id=payload.user_id,
        payload=payload,
        db=db
    )

    return {
        "message": "Education qualification added successfully",
        "user_id":payload.user_id,
        "education_id": education.id
    }
