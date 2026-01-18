from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.student_certificate import StudentCertificate
from schemas.student_education_schema import (
    StudentCertificateCreate,
    StudentNOCUpdate
)

# from models.user_registration import UserRegistration
# from models.student_qualification import StudentQualification
# from models.generated_models import JobOpenings
from models.generated_models import UserRegistration,StudentQualification,JobOpenings,JobApplication
from schemas.student_education_schema import JobOpeningCreate

from sqlalchemy.orm import Session
# from models.generated_models import JobApplication
from schemas.student_education_schema import JobApplicationCreate




##job openings

def create_job_openings(db:Session,data:JobOpeningCreate,user_id:int):
    job=JobOpenings(**data.model_dump(),created_by=user_id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_job_openings(db: Session):
    return db.query(JobOpenings).filter(JobOpenings.is_active == True).all()


def get_job_opening(db: Session, job_id: int):
    job = db.query(JobOpenings).filter(JobOpenings.id == job_id).first()
    if not job:
        raise HTTPException(404, "Job not found")
    return job

def delete_job_opening_service(db: Session,job_id: int,user_id: int):
    job = (
        db.query(JobOpenings)
        .filter(
            JobOpenings.id == job_id,
            JobOpenings.created_by == user_id,
            JobOpenings.is_active == True
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job opening not found or not authorized"
        )

    job.is_active = False  
    db.commit()

    return {"message": "Job opening deleted successfully"}




def apply_job_service(db: Session,payload: JobApplicationCreate,user_id: int):
    application = JobApplication(**payload.model_dump(),user_id=user_id)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application







# ================= CERTIFICATION =================

def create_student_certificate(
    db: Session,
    data: StudentCertificateCreate
):
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


def get_student_certificates(db: Session, user_id: int):
    return db.query(StudentCertificate).filter(
        StudentCertificate.user_id == user_id,
        StudentCertificate.is_active == True
    ).all()


# ================= NOC =================

def update_student_noc(
    db: Session,
    data: StudentNOCUpdate
):
    user = db.query(UserRegistration).filter(
        UserRegistration.id == data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.noc_number = data.noc_number
    user.police_station_name = data.police_station_name
    user.issue_year = data.issue_year
    user.upload_noc = data.upload_noc

    db.commit()
    db.refresh(user)
    return user


# ================= EDUCATION / QUALIFICATION =================

EDUCATION_ROLE_ID = 8


def add_student_education_service(
    user_id: int,
    payload,
    db: Session
):
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
        raise HTTPException(
            status_code=404,
            detail="Education student not found"
        )

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
