from sqlalchemy.orm import Session
from sqlalchemy import text, cast, Float, desc
from core.database import SessionLocal
from models.user_registration import UserRegistration
from models.student_qualification import StudentQualification

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
    students = (
        db.query(
            UserRegistration.first_name,
            UserRegistration.last_name,
            UserRegistration.is_active,
            StudentQualification.institute,
            StudentQualification.degree,
            cast(StudentQualification.percentage, Float).label("percentage")
        )
        .join(StudentQualification, StudentQualification.user_id == UserRegistration.id)
        .filter(
            cast(StudentQualification.percentage, Float) >= 90,
            UserRegistration.is_active.is_(True),
            StudentQualification.is_active.is_(True)
        )
        .order_by(desc(cast(StudentQualification.percentage, Float)))
        .all()
    )

    return [
        {
            "full_name": f"{s.first_name} {s.last_name}",
            "institute": s.institute,
            "degree": s.degree,
            "attendance_percentage": float(s.percentage),
            "active": bool(s.is_active)
        }
        for s in students
    ]