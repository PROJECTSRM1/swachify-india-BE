from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import text

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, status
from models.student_certificate import StudentCertificate
from models.generated_models import UserRegistration, StudentQualification, JobOpenings, JobApplication
from schemas.student_education_schema import (
    StudentCertificateCreate,
    StudentNOCUpdate,
    JobOpeningCreate,
    JobApplicationCreate,
    StudentEducationCreate
)


##job openings

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
        .filter(
            JobOpenings.id == opening_id,
            JobOpenings.is_active == True
        )
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

def create_student_certificate(db: Session, data: StudentCertificateCreate) -> StudentCertificate:
    record = StudentCertificate(
        user_id=data.user_id,
        certificate_name=data.certificate_name,
        issued_by=data.issued_by,
        year=data.year,
        upload_certificate=data.upload_certificate,
        created_by=data.user_id,
        is_active=True
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_student_certificates(db: Session, user_id: int) -> list[StudentCertificate]:
    return db.query(StudentCertificate).filter(
        StudentCertificate.user_id == user_id,
        StudentCertificate.is_active == True
    ).all()


# ================= NOC =================

def update_student_noc(db: Session, data: StudentNOCUpdate) -> UserRegistration:
    user = db.query(UserRegistration).filter(
        UserRegistration.id == data.user_id
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.noc_number = data.noc_number
    user.police_station_name = data.police_station_name
    user.issue_year = data.issue_year
    user.upload_noc = data.upload_noc

    db.commit()
    db.refresh(user)
    return user


# ================= EDUCATION / QUALIFICATION =================

def add_student_education_service(user_id: int, payload: StudentEducationCreate, db: Session) -> StudentQualification:
    # Check education student exists
    student = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == user_id,
            UserRegistration.is_active == True
        )
        .first()
    )

    if not student:
        raise HTTPException(status_code=404, detail="Education student not found")

    # Insert qualification
    education = StudentQualification(
        user_id=user_id,
        degree=payload.degree,
        institute=payload.institute,
        percentage=payload.percentage
    )

    db.add(education)
    db.commit()
    db.refresh(education)

    return education

def get_students_list_service(
    db: Session,
    skill_id: int | None = None,
    aggregate: str | None = None,
    internship_status: str | None = None
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
            "internship_status": internship_status
        }
    ).mappings().all()
