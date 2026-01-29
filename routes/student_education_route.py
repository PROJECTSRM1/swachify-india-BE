from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db

from schemas.student_education_schema import (
    StudentListResponse,
    StudentProfileResponse,
    StudentEducationFullCreate,
)

from schemas.student_attendance_schema import (
    StudentAttendanceCreate,
    StudentAttendanceResponse,
)

from schemas.student_internship_status import (
    StudentInternshipStatusCreate,
    StudentInternshipStatusResponse,
)

from services.student_education_service import (
    create_student_certificate,
    add_student_education_service,
    get_internship_list_service,
    get_recent_joiners_service,
    update_student_noc,
    get_students_list_service,
    get_top_performers_service,
)

from services.student_attendance_service import upsert_student_attendance
from services.student_internship_service import upsert_student_internship

from models.generated_models import UserRegistration
from models.generated_models import StudentCertificate
from models.generated_models import StudentQualification

router = APIRouter(
    prefix="/api/education",
    tags=["Student Education"]
)

# =====================================================
# STUDENT LIST (NO DUPLICATES)
# =====================================================

@router.get("/students-list")
def get_students_list(
    skill_id: int | None = None,
    aggregate: str | None = None,
    internship_status: str | None = None,
    db: Session = Depends(get_db),
):
    return get_students_list_service(
        db=db,
        skill_id=skill_id,
        aggregate=aggregate,
        internship_status=internship_status
    )

# =====================================================
# STUDENT FULL PROFILE
# =====================================================

@router.get(
    "/students/{student_id}/full-profile",
)
def get_full_student_profile(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == student_id,
            UserRegistration.is_active == True
        )
        .first()
    )

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    education = (
        db.query(StudentQualification)
        .filter(
            StudentQualification.user_id == student_id,
            StudentQualification.is_active == True
        )
        .all()
    )

    certificates = (
        db.query(StudentCertificate)
        .filter(
            StudentCertificate.user_id == student_id,
            StudentCertificate.is_active == True
        )
        .all()
    )

    return {
        "profile": StudentProfileResponse(
            user_id=student.id,
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            mobile_number=student.mobile,
            government_id=student.government_id,
            location=student.address,
            service_name="Education"
        ),
        "education": education,
        "certificates": certificates,
        "noc": {
            "noc_number": student.noc_number,
            "police_station_name": student.police_station_name,
            "issue_year": student.issue_year,
            "upload_noc": student.upload_noc
        }
    }

# =====================================================
# ADD FULL STUDENT PROFILE DATA
# =====================================================

@router.post(
    "/students/{student_id}/full-profile"
    )
def add_full_student_profile(
    student_id: int,
    payload: StudentEducationFullCreate,
    db: Session = Depends(get_db),
):
    results = {}

    if payload.education:
        results["education"] = []
        for edu in payload.education:
            record = add_student_education_service(
                db=db,
                student_id=student_id,
                payload=edu,
            )
            results["education"].append(record.id)

    if payload.certificates:
        results["certificates"] = []
        for cert in payload.certificates:
            record = create_student_certificate(
                db=db,
                student_id=student_id,
                payload=cert,
            )
            results["certificates"].append(record.id)

    if payload.noc:
        user = update_student_noc(
            db=db,
            student_id=student_id,
            payload=payload.noc,
        )
        results["noc_updated_for_user"] = user.id

    if not results:
        raise HTTPException(status_code=400, detail="No valid data provided")

    return {
        "message": "Student profile updated successfully",
        "data": results
    }

# =====================================================
# ATTENDANCE
# =====================================================

@router.post(
    "/students/{student_id}/attendance",
    response_model=StudentAttendanceResponse,
)
def update_student_attendance(
    student_id: int,
    payload: StudentAttendanceCreate,
    db: Session = Depends(get_db),
):
    return upsert_student_attendance(
        db=db,
        user_id=student_id,
        attendance_percentage=payload.attendance_percentage,
    )

# =====================================================
# INTERNSHIP STATUS
# =====================================================

@router.post(
    "/students/{student_id}/internship-status",
    response_model=StudentInternshipStatusResponse,
)
def update_student_internship_status(
    student_id: int,
    payload: StudentInternshipStatusCreate,
    db: Session = Depends(get_db),
):
    return upsert_student_internship(
        db=db,
        user_id=student_id,
        internship_status=payload.internship_status,
    )

@router.get(
    "/students/top-performers",
    response_model=List[StudentListResponse],
)
def get_top_performers(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_top_performers_service(db, limit)

@router.get(
    "/students/recent-joiners",
    response_model=List[StudentListResponse],
)
def get_recent_joiners(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_recent_joiners_service(db, limit)



from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from core.database import get_db

@router.get("/", response_model=List[Dict[str, Any]])
def get_internships(
    category_id: int = Query(-1, description="Category ID (-1 = all)"),
    work_type_id: int = Query(-1, description="Work Type ID (-1 = all)"),
    db: Session = Depends(get_db)
):
    return get_internship_list_service(
        db=db,
        category_id=category_id,
        work_type_id=work_type_id
    )