from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import text

from models.generated_models import (
    UserRegistration,
    StudentQualification,
    StudentCertificate,
    JobOpenings,
    JobApplication,
)

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

    # ✅ DUPLICATE CHECK
    existing = (
        db.query(StudentCertificate)
        .filter(
            StudentCertificate.user_id == student_id,
            StudentCertificate.certificate_name == payload.certificate_name,
            StudentCertificate.issued_by == payload.issued_by,
            StudentCertificate.year == payload.year,
            StudentCertificate.is_active == True,
        )
        .first()
    )

    if existing:
        return existing

    record = StudentCertificate(
        user_id=student_id,
        certificate_name=payload.certificate_name,
        issued_by=payload.issued_by,
        year=payload.year,
        upload_certificate=payload.upload_certificate,
        created_by=student_id,
        is_active=True,
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


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

    # ✅ DUPLICATE CHECK
    existing = (
        db.query(StudentQualification)
        .filter(
            StudentQualification.user_id == student_id,
            StudentQualification.degree == payload.degree,
            StudentQualification.institute == payload.institute,
            StudentQualification.percentage == payload.percentage,
            StudentQualification.is_active == True,
        )
        .first()
    )

    if existing:
        return existing

    education = StudentQualification(
        user_id=student_id,
        degree=payload.degree,
        institute=payload.institute,
        percentage=payload.percentage,
        is_active=True,
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
    sort_by: str | None = None,   # expected value: "both"
):
    # =====================================================
    # 1️⃣ Student summary (from VIEW)
    # =====================================================
    rows = db.execute(
        text("""
            SELECT *
            FROM vw_students_get_list
            WHERE
              (:skill_id IS NULL OR skill_id = :skill_id)
            AND (:aggregate IS NULL OR aggregate = :aggregate)
            AND (:internship_status IS NULL OR internship_status = :internship_status)
        """),
        {
            "skill_id": skill_id,
            "aggregate": aggregate,
            "internship_status": internship_status,
        },
    ).mappings().all()

    students: dict[int, dict] = {}

    for row in rows:
        user_id = row["user_id"]

        if user_id not in students:
            students[user_id] = {
                "user_id": user_id,
                "student_name": row["student_name"],
                "joined_date": row["joined_date"],
                "skill_id": row["skill_id"],
                "skill": row["skill"],
                "attendance_percentage": row["attendance_percentage"],
                "aggregate": row["aggregate"],
                "internship_status": row["internship_status"],
                "rating": row["rating"],
                "education": [],
                "certificates": [],
                # internal sets for deduplication
                "_edu_keys": set(),
                "_cert_keys": set(),
            }

    if not students:
        return []

    user_ids = list(students.keys())

    # =====================================================
    # 2️⃣ Education (TABLE) — with de-duplication
    # =====================================================
    educations = (
        db.query(StudentQualification)
        .filter(
            StudentQualification.user_id.in_(user_ids),
            StudentQualification.is_active == True
        )
        .all()
    )

    for edu in educations:
        key = (edu.degree, edu.institute, edu.percentage)

        if key not in students[edu.user_id]["_edu_keys"]:
            students[edu.user_id]["_edu_keys"].add(key)
            students[edu.user_id]["education"].append({
                "degree": edu.degree,
                "institute": edu.institute,
                "percentage": edu.percentage,
            })

    # =====================================================
    # 3️⃣ Certificates (TABLE) — with de-duplication
    # =====================================================
    certificates = (
        db.query(StudentCertificate)
        .filter(
            StudentCertificate.user_id.in_(user_ids),
            StudentCertificate.is_active == True
        )
        .all()
    )

    for cert in certificates:
        key = (
            cert.certificate_name,
            cert.issued_by,
            cert.year,
            cert.upload_certificate
        )

        if key not in students[cert.user_id]["_cert_keys"]:
            students[cert.user_id]["_cert_keys"].add(key)
            students[cert.user_id]["certificates"].append({
                "id": cert.id,
                "certificate_name": cert.certificate_name,
                "issued_by": cert.issued_by,
                "year": cert.year,
                "upload_certificate": cert.upload_certificate,
                "is_active": cert.is_active,
            })

    # =====================================================
    # 4️⃣ Remove internal dedup keys
    # =====================================================
    for s in students.values():
        s.pop("_edu_keys")
        s.pop("_cert_keys")

    students_list = list(students.values())

    # =====================================================
    # 5️⃣ SORT BY BOTH (rating → attendance)
    # =====================================================
    if sort_by == "both":
        students_list.sort(
            key=lambda s: (
                float(s["rating"] or 0),
                float(s["attendance_percentage"] or 0)
            ),
            reverse=True
        )

    return students_list


def get_top_performers_service(
    db: Session,
    limit: int = 10
):
    """
    Top performers = students sorted by BOTH (rating + attendance)
    """
    students = get_students_list_service(
        db=db,
        sort_by="both"   # rating first, attendance second
    )

    return students[:limit]

def get_recent_joiners_service(
    db: Session,
    limit: int = 10,
    min_rating: float | None = None,
):
    students = get_students_list_service(db=db)

    # ✅ rating filter
    if min_rating is not None:
        students = [
            s for s in students
            if s["rating"] is not None and float(s["rating"]) >= min_rating
        ]

    # ✅ recent joiners
    students.sort(
        key=lambda s: s["joined_date"] or 0,
        reverse=True
    )

    return students[:limit]


def get_active_job_openings(db: Session, category_id: int = -1):
    query = text("""
        SELECT *
        FROM vw_active_job_openings
        WHERE (:category_id = -1 OR category_id = :category_id)
    """)

    return db.execute(
        query,
        {"category_id": category_id}
    ).mappings().all()