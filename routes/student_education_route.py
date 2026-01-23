from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.student_education_schema import (
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
    update_student_noc,
    get_students_list_service,
)
from services.student_attendance_service import upsert_student_attendance
from services.student_internship_service import upsert_student_internship

from models.generated_models import UserRegistration
from models.student_certificate import StudentCertificate
from models.student_qualification import StudentQualification

router = APIRouter(
    prefix="/api/education",
    tags=["Student Education"]
)


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
        internship_status=internship_status,
    )


@router.get("/students/{student_id}/full-profile")
def get_full_student_profile(student_id: int, db: Session = Depends(get_db)):
    """
    Get all education, certificates, and NOC for a student in a single response.
    """
    student = db.query(UserRegistration).filter(UserRegistration.id == student_id, UserRegistration.is_active == True).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    education = db.query(StudentQualification).filter(StudentQualification.user_id == student_id, StudentQualification.is_active == True).all()
    certificates = db.query(StudentCertificate).filter(StudentCertificate.user_id == student_id, StudentCertificate.is_active == True).all()
    noc = {
        "noc_number": getattr(student, "noc_number", None),
        "police_station_name": getattr(student, "police_station_name", None),
        "issue_year": getattr(student, "issue_year", None),
        "upload_noc": getattr(student, "upload_noc", None)
    }
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
        "education": [
            {"degree": e.degree, "institute": e.institute, "percentage": e.percentage} for e in education
        ],
        "certificates": [
            {"certificate_name": c.certificate_name, "issued_by": c.issued_by, "year": c.year, "upload_certificate": c.upload_certificate} for c in certificates
        ],
        "noc": noc
    }

@router.post("/students/{student_id}/full-profile")
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
            results["education"].append({"education_id": record.id})

    if payload.certificates:
        results["certificates"] = []
        for cert in payload.certificates:
            record = create_student_certificate(
                db=db,
                student_id=student_id,
                payload=cert,
            )
            results["certificates"].append({"certificate_id": record.id})

    if payload.noc:
        user = update_student_noc(
            db=db,
            student_id=student_id,
            payload=payload.noc,
        )
        results["noc"] = {"user_id": user.id}

    if not results:
        raise HTTPException(status_code=400, detail="No valid data provided")

    return {
        "message": "Student profile updated successfully",
        **results,
    }

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
