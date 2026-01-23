from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import text

from models.generated_models import (
    UserRegistration,
    StudentQualification,
    JobOpenings,
    JobApplication,
)
from models.student_certificate import StudentCertificate

from schemas.student_education_schema import (
    StudentCertificateCreate,
    StudentNOCUpdate,
    JobOpeningCreate,
    JobApplicationCreate,
    StudentEducationCreate,
)

def create_job_openings(db: Session, data: JobOpeningCreate, user_id: int) -> JobOpenings:
    job = JobOpenings(**data.model_dump(), created_by=user_id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job_openings(db: Session) -> list[JobOpenings]:
    return db.query(JobOpenings).filter(JobOpenings.is_active == True).all()


def get_job_opening(db: Session, job_id: int) -> JobOpenings:
    job = db.query(JobOpenings).filter(JobOpenings.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


def delete_job_opening_service(db: Session, opening_id: int, user_id: int) -> dict:
    job_opening = (
        db.query(JobOpenings)
        .filter(JobOpenings.id == opening_id, JobOpenings.is_active == True)
        .first()
    )

    if not job_opening:
        raise HTTPException(status_code=404, detail="Job opening not found")

    if job_opening.created_by != user_id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this job opening")

    job_opening.is_active = False
    job_opening.modified_by = user_id
    db.commit()

    return {"message": "Job opening deleted successfully"}

def apply_job_service(db: Session, payload: JobApplicationCreate, user_id: int) -> JobApplication:
    application = JobApplication(**payload.model_dump(), user_id=user_id)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


# ================= CERTIFICATION =================

def create_student_certificate(
    db: Session,
    student_id: int,
    payload: StudentCertificateCreate
) -> StudentCertificate:

    student = (
        db.query(UserRegistration)
        .filter(UserRegistration.id == student_id, UserRegistration.is_active == True)
        .first()
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    record = StudentCertificate(
        user_id=student_id,
        certificate_name=payload.certificate_name,
        issued_by=payload.issued_by,
        year=payload.year,
        upload_certificate=payload.upload_certificate,
        created_by=student_id,
        is_active=True
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_student_certificates(db: Session, student_id: int) -> list[StudentCertificate]:
    return (
        db.query(StudentCertificate)
        .filter(
            StudentCertificate.user_id == student_id,
            StudentCertificate.is_active == True
        )
        .all()
    )


# ================= NOC =================

def update_student_noc(
    db: Session,
    student_id: int,
    payload: StudentNOCUpdate
) -> UserRegistration:

    user = (
        db.query(UserRegistration)
        .filter(UserRegistration.id == student_id, UserRegistration.is_active == True)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    user.noc_number = payload.noc_number
    user.police_station_name = payload.police_station_name
    user.issue_year = payload.issue_year
    user.upload_noc = payload.upload_noc

    db.commit()
    db.refresh(user)
    return user


# ================= EDUCATION / QUALIFICATION =================

def add_student_education_service(
    db: Session,
    student_id: int,
    payload: StudentEducationCreate
) -> StudentQualification:

    student = (
        db.query(UserRegistration)
        .filter(UserRegistration.id == student_id, UserRegistration.is_active == True)
        .first()
    )

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    education = StudentQualification(
        user_id=student_id,
        degree=payload.degree,
        institute=payload.institute,
        percentage=payload.percentage,
    )

    db.add(education)
    db.commit()
    db.refresh(education)
    return education


def get_students_list_service(
    db: Session,
    skill_id: int | None = None,
    aggregate: str | None = None,
    internship_status: str | None = None,
):
    query = text("""
        SELECT *
        FROM vw_students_get_list
        WHERE
          (:skill_id IS NULL OR skill_id = :skill_id)
        AND (:aggregate IS NULL OR aggregate = :aggregate)
        AND (:internship_status IS NULL OR internship_status = :internship_status)
    """)

    return db.execute(
        query,
        {
            "skill_id": skill_id,
            "aggregate": aggregate,
            "internship_status": internship_status,
        },
    ).mappings().all()
