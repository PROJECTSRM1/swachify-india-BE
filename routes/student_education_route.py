from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from schemas.student_education_schema import (
    StudentCertificateCreate, StudentProfileResponse, StudentEducationCreate, StudentNOCUpdate, StudentEducationFullCreate
)
from services.student_education_service import (
    create_student_certificate,
    get_student_certificates,
    add_student_education_service,
    update_student_noc,
    get_students_list_service,
)
from models.generated_models import UserRegistration, UserServices, MasterModule
from models.student_certificate import StudentCertificate
from models.student_qualification import StudentQualification



router = APIRouter(prefix="/api/education", tags=["Student Education"])



# ========== Student List & Detail ==========

@router.get("/students-list")
def get_students_list(skill_id: int = None, aggregate: str = None, internship_status: str = None, db: Session = Depends(get_db)):
    """
    List all students, with optional filters for skill, aggregate, and internship status.
    """
    return get_students_list_service(db=db, skill_id=skill_id, aggregate=aggregate, internship_status=internship_status)


@router.get("/students/{student_id}")
def get_student_details(student_id: int, db: Session = Depends(get_db)):
    """
    Get full details for a student: profile, education, certificates, NOC.
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

# 2. Get student details (profile, education, certificates, NOC)
@router.get("/students/{student_id}")
def get_student_details(student_id: int, db: Session = Depends(get_db)):
    """
    Returns full details for a student:
    - Profile info
    - Education records
    - Certificates
    - NOC status
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
            {
                "degree": e.degree,
                "institute": e.institute,
                "percentage": e.percentage
            } for e in education
        ],
        "certificates": [
            {
                "certificate_name": c.certificate_name,
                "issued_by": c.issued_by,
                "year": c.year,
                "upload_certificate": c.upload_certificate
            } for c in certificates
        ],
        "noc": noc
    }


# ========== Student Education ==========
@router.get("/students/{student_id}/education")
def get_student_education(student_id: int, db: Session = Depends(get_db)):
    """
    Get all education records for a student.
    """
    education = db.query(StudentQualification).filter(StudentQualification.user_id == student_id, StudentQualification.is_active == True).all()
    return [
        {"degree": e.degree, "institute": e.institute, "percentage": e.percentage} for e in education
    ]

@router.post("/students/{student_id}/education")
def add_student_education_by_id(student_id: int, payload: StudentEducationCreate, db: Session = Depends(get_db)):
    """
    Add a new education record for a student.
    """
    education = add_student_education_service(user_id=student_id, payload=payload, db=db)
    return {"message": "Education qualification added successfully", "user_id": student_id, "education_id": education.id}


# ========== Student Certificates ==========
@router.get("/students/{student_id}/certificates")
def get_student_certificates_by_id(student_id: int, db: Session = Depends(get_db)):
    """
    Get all certificates for a student.
    """
    certificates = db.query(StudentCertificate).filter(StudentCertificate.user_id == student_id, StudentCertificate.is_active == True).all()
    return [
        {"certificate_name": c.certificate_name, "issued_by": c.issued_by, "year": c.year, "upload_certificate": c.upload_certificate} for c in certificates
    ]

@router.post("/students/{student_id}/certificates")
def add_student_certificate_by_id(student_id: int, payload: StudentCertificateCreate, db: Session = Depends(get_db)):
    """
    Add a new certificate for a student.
    """
    cert = create_student_certificate(db, payload)
    return {"message": "Certificate added successfully", "user_id": student_id, "certificate_id": cert.id}


@router.post("/students/{student_id}/full-profile")
def add_full_student_profile(student_id: int, payload: StudentEducationFullCreate, db: Session = Depends(get_db)):
    """
    Add education, certificates, and/or NOC for a student in a single request.
    """
    results = {}
    # Add education records
    if payload.education:
        results["education"] = []
        for edu in payload.education:
            edu.user_id = student_id
            education = add_student_education_service(user_id=student_id, payload=edu, db=db)
            results["education"].append({"education_id": education.id})
    # Add certificates
    if payload.certificates:
        results["certificates"] = []
        for cert in payload.certificates:
            cert.user_id = student_id
            certificate = create_student_certificate(db, cert)
            results["certificates"].append({"certificate_id": certificate.id})
    # Add/update NOC
    if payload.noc:
        payload.noc.user_id = student_id
        noc = update_student_noc(db, payload.noc)
        results["noc"] = {"user_id": noc.id}
    if not results:
        raise HTTPException(status_code=400, detail="No valid data provided.")
    return {"message": "Student profile updated successfully", **results}

# ========== Student NOC ========== 
@router.get("/students/{student_id}/noc")
def get_student_noc(student_id: int, db: Session = Depends(get_db)):
    """
    Get NOC status for a student.
    """
    student = db.query(UserRegistration).filter(UserRegistration.id == student_id, UserRegistration.is_active == True).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "noc_number": getattr(student, "noc_number", None),
        "police_station_name": getattr(student, "police_station_name", None),
        "issue_year": getattr(student, "issue_year", None),
        "upload_noc": getattr(student, "upload_noc", None)
    }

@router.put("/students/{student_id}/noc")
def update_student_noc_by_id(student_id: int, payload: StudentNOCUpdate, db: Session = Depends(get_db)):
    """
    Update NOC status for a student.
    """
    user = update_student_noc(db, payload)
    return {
        "user_id": user.id,
        "noc_number": user.noc_number,
        "police_station_name": user.police_station_name,
        "issue_year": user.issue_year,
        "upload_noc": user.upload_noc
    }

@router.get("/students/{student_id}/education")
def get_student_education(student_id: int, db: Session = Depends(get_db)):
        education = db.query(StudentQualification).filter(StudentQualification.user_id == student_id, StudentQualification.is_active == True).all()
        return [
            {
                "degree": e.degree,
                "institute": e.institute,
                "percentage": e.percentage
            } for e in education
        ]

@router.post("/students/{student_id}/education")
def add_student_education_by_id(payload: StudentEducationCreate, db: Session = Depends(get_db)):
        education = add_student_education_service( payload=payload, db=db)
        return {
            "message": "Education qualification added successfully",
            "user_id": payload.user_id,
            "education_id": education.id
        }

    # 5. Student certificates (GET/POST)
@router.get("/students/{student_id}/certificates")
def get_student_certificates_by_id(student_id: int, db: Session = Depends(get_db)):
        certificates = db.query(StudentCertificate).filter(StudentCertificate.user_id == student_id, StudentCertificate.is_active == True).all()
        return [
            {
                "certificate_name": c.certificate_name,
                "issued_by": c.issued_by,
                "year": c.year,
                "upload_certificate": c.upload_certificate
            } for c in certificates
        ]

@router.post("/students/{student_id}/certificates")
def add_student_certificate_by_id(payload: StudentCertificateCreate, db: Session = Depends(get_db)):
        cert = create_student_certificate(db, payload)
        return {
            "message": "Certificate added successfully",
            "user_id": payload.user_id,
            "certificate_id": cert.id
        }

    # 6. Student NOC (GET/PUT)
@router.get("/students/{student_id}/noc")
def get_student_noc(student_id: int, db: Session = Depends(get_db)):
        student = db.query(UserRegistration).filter(UserRegistration.id == student_id, UserRegistration.is_active == True).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return {
            "noc_number": getattr(student, "noc_number", None),
            "police_station_name": getattr(student, "police_station_name", None),
            "issue_year": getattr(student, "issue_year", None),
            "upload_noc": getattr(student, "upload_noc", None)
        }

@router.put("/students/{student_id}/noc")
def update_student_noc_by_id(payload: StudentNOCUpdate, db: Session = Depends(get_db)):
        user = update_student_noc(db, payload)
        return {
            "user_id": user.id,
            "noc_number": user.noc_number,
            "police_station_name": user.police_station_name,
            "issue_year": user.issue_year,
            "upload_noc": user.upload_noc
        }