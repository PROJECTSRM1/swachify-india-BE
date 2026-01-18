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

from models.generated_models import UserRegistration, MasterModule


router = APIRouter(prefix="/api/student/education", tags=["Student Education"])
bearer_scheme = HTTPBearer() 

@router.post("/certifications")
def add_certificate(
    payload: StudentCertificateCreate,
    db: Session = Depends(get_db),
):
    return create_student_certificate(db, payload)


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


# @router.get(
#     "/profile",
#     response_model=StudentProfileResponse,
#     dependencies=[Security(bearer_scheme)]
# )

# def get_student_profile(
#     current_user: UserRegistration = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     user_id = current_user.id
#     student = (
#         db.query(UserRegistration)
#         .filter(
#             UserRegistration.id == user_id,
#             UserRegistration.services.any(
#                 MasterModule.module_name == "Education"
#             )
#         )
#         .first()
#     )

#     if not student:
#         raise HTTPException(
#             status_code=404,
#             detail="Student profile not found"
#         )

#     return StudentProfileResponse(
#         user_id=student.id, 
#         first_name=student.first_name,
#         last_name=student.last_name,
#         email=student.email,
#         mobile_number=student.mobile,
#         government_id=student.government_id,
#         location=student.address,
#         service_name="Education"
#     )


@router.get(
    "/profile",
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
            UserRegistration.is_active == True
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
