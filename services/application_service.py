from sqlalchemy.orm import Session
from sqlalchemy import func,  text, cast, Float, desc
from core.database import SessionLocal
from models.generated_models import UserRegistration
from models.generated_models import StudentQualification
###
from datetime import datetime
from models.generated_models import JobOpenings

from fastapi import HTTPException, status

from models.generated_models import JobOpenings
from models.generated_models import MasterJob


#### ADDED


def create_job_opening(db: Session, payload):
    user = (
        db.query(UserRegistration)
        .filter(UserRegistration.id == payload.created_by)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid created_by: user does not exist"
        )

    job = JobOpenings(
        job_id=payload.job_id,
        company_name=payload.company_name,
        company_address=payload.company_address,
        location_type_id=payload.location_type_id,
        work_type_id=payload.work_type_id,
        role_description=payload.role_description,
        requirements=payload.requirements,
        sub_module_id=payload.sub_module_id,
        category_id=payload.category_id,
        internship_duration_id=payload.internship_duration_id,
        stipend_type_id=payload.stipend_type_id,
        internship_stipend=payload.internship_stipend,
        # created_by=user_id,
        created_by=payload.created_by,
        created_date=datetime.utcnow(),
        is_active=True
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job_openings(
    db: Session,
    job_id: int | None = None,
    category_id: int | None = None,
    location_type_id: int | None = None
):
    query = db.query(JobOpenings).filter(JobOpenings.is_active)

    # 🔹 filter by job id (single job)
    if job_id is not None:
        return query.filter(JobOpenings.id == job_id).first()

    # 🔹 filter by category
    if category_id is not None:
        query = query.filter(JobOpenings.category_id == category_id)

    # 🔹 filter by location_type_id
    if location_type_id is not None:
        query = query.filter(JobOpenings.location_type_id == location_type_id)

    # 🔹 default → all jobs
    return query.order_by(JobOpenings.created_date.desc()).all()


def get_application_review(user_id: int):
    db: Session = SessionLocal()

    query = """
    SELECT 
        CONCAT(ur.first_name, ' ', ur.last_name) AS full_name,
        ur.dob,
        ur.gender_id::text AS gender,
        ur.email,
        ur.mobile AS phone,

        sq.degree,
        sq.institute,
        sq.percentage,

        '' AS application_code,
        '' AS status,
        '' AS internship_title,
        '' AS company,
        '' AS location

    FROM user_registration ur
    LEFT JOIN student_qualification sq 
        ON sq.user_id = ur.id AND sq.is_active = true

    WHERE ur.id = :user_id
    """

    row = db.execute(text(query), {"user_id": user_id}).fetchone()

    if not row:
        return None

    data = dict(row._mapping)

    # ✅ Convert DOB to string
    if data.get("dob"):
        data["dob"] = data["dob"].strftime("%Y-%m-%d")
    else:
        data["dob"] = ""

    # ✅ Replace None with empty string for Swagger
    for key in data:
        if data[key] is None:
            data[key] = ""

    return data




def update_application(user_id: int, data):
    db: Session = SessionLocal()

    payload = data.dict(exclude_unset=True)

    # ---------------- USER REGISTRATION ----------------
    if any(k in payload for k in ["full_name", "dob", "gender", "email", "phone"]):
        first_name = ""
        last_name = ""

        if payload.get("full_name"):
            parts = payload["full_name"].split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

        db.execute(text("""
            UPDATE user_registration
            SET first_name = COALESCE(:first_name, first_name),
                last_name = COALESCE(:last_name, last_name),
                dob = COALESCE(:dob, dob),
                gender_id = COALESCE(:gender, gender_id),
                email = COALESCE(:email, email),
                mobile = COALESCE(:phone, mobile)
            WHERE id = :user_id
        """), {
            "first_name": first_name or None,
            "last_name": last_name or None,
            "dob": payload.get("dob"),
            "gender": payload.get("gender"),
            "email": payload.get("email"),
            "phone": payload.get("phone"),
            "user_id": user_id
        })

    # ---------------- STUDENT QUALIFICATION ----------------
    if any(k in payload for k in ["degree", "institute", "percentage"]):
        db.execute(text("""
            UPDATE student_qualification
            SET degree = COALESCE(:degree, degree),
                institute = COALESCE(:institute, institute),
                percentage = COALESCE(:percentage, percentage)
            WHERE user_id = :user_id
        """), {
            "degree": payload.get("degree"),
            "institute": payload.get("institute"),
            "percentage": payload.get("percentage"),
            "user_id": user_id
        })

    # ---------------- JOB APPLICATION (OPTIONAL) ----------------
    if any(k in payload for k in ["application_code", "status"]):
        db.execute(text("""
            UPDATE job_application
            SET application_code = COALESCE(:application_code, application_code),
                status = COALESCE(:status, status)
            WHERE user_id = :user_id
        """), {
            "application_code": payload.get("application_code"),
            "status": payload.get("status"),
            "user_id": user_id
        })

    # ---------------- JOB OPENINGS (OPTIONAL) ----------------
    if any(k in payload for k in ["internship_title", "company", "location"]):
        db.execute(text("""
            UPDATE job_openings
            SET title = COALESCE(:internship_title, title),
                company = COALESCE(:company, company),
                location = COALESCE(:location, location)
            WHERE job_id = (
                SELECT job_id FROM job_application WHERE user_id = :user_id
            )
        """), {
            "internship_title": payload.get("internship_title"),
            "company": payload.get("company"),
            "location": payload.get("location"),
            "user_id": user_id
        })

    db.commit()




 

def get_trending_students(db: Session):

    percentage_clean = cast(
        func.replace(StudentQualification.percentage, '%', ''),
        Float
    )

    students = (
        db.query(
            UserRegistration.first_name,
            UserRegistration.last_name,
            UserRegistration.is_active,
            StudentQualification.institute,
            StudentQualification.degree,
            percentage_clean.label("percentage")
        )
        .join(StudentQualification, StudentQualification.user_id == UserRegistration.id)
        .filter(
            percentage_clean.isnot(None),
            percentage_clean >= 80,
            UserRegistration.is_active.is_(True),
            StudentQualification.is_active.is_(True)
        )
        .order_by(desc(percentage_clean))
        .all()
    )

    return [
        {
            "full_name": f"{s.first_name} {s.last_name}",
            "institute": s.institute,
            "degree": s.degree,
            "attendance_percentage": float(s.percentage) if s.percentage else 0,
            "active": bool(s.is_active)
        }
        for s in students
    ]





 
 # ✅ CONDITION 1 — FETCH MASTER JOB BY ID
def fetch_master_job(db: Session, master_job_id: int):
    return (
        db.query(MasterJob)
        .filter(MasterJob.id == master_job_id)
        .first()
    )

 
 
def fetch_success_ui_by_job_id(db: Session, job_id: int):
    # Join job_openings with master_job
    data = (
        db.query(
            JobOpenings.id.label("job_opening_id"),
            JobOpenings.company_name,
            JobOpenings.is_active,
            MasterJob.job_name
        )
        .join(MasterJob, JobOpenings.job_id == MasterJob.id)
        .filter(JobOpenings.job_id == job_id)
        .first()
    )

    if not data:
        return None

    job_opening_id = data.job_opening_id
    position = data.job_name
    company = data.company_name
    status = "RECEIVED" if data.is_active else "INACTIVE"

     # ✅ Application ID is ONLY numeric
    application_id = job_opening_id

    return {
        # "success": True,
        # "title": "Congratulations, Alex!",
        "message": f"Your application for the {position} has been submitted successfully.",
        "application_details": {
            "position": position,
            "company": company,
            "application_id": application_id,
            # "status": status.upper()
        }
    }