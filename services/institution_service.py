from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException,status

from models.generated_models import (
    BusAlertLog,
    BusFleet,
    EnrollmentStatus,
    EnrollmentStatus,
    InstitutionRegistration,
    InstitutionBranch,
    MaintenanceBudget,
    PayrollSummary,
    StaffPayslip,
    StaffProfile,
    StudentProfile
)
from sqlalchemy import text
from typing import List
from schemas.institution_schema import (
    BusAlertCreate,
    BusAlertUpdate,
    EnrollmentStatusCreate,
    InstitutionRegistrationCreate,
    InstitutionBranchCreate,
    MaintenanceBudgetCreate,
    PayrollSummaryCreate,
    StaffPayslipCreate,
    StaffProfileCreate,
    StudentAcademicDetailsSchema,
    StudentProfileCreate,
    StudentProfileUpdate
)



# ======================================================
# INSTITUTION REGISTRATION SERVICES
# ======================================================

def create_institution(
    db: Session,
    payload: InstitutionRegistrationCreate
):
    institution = InstitutionRegistration(
        **payload.dict(),
        created_date=datetime.utcnow()
    )
    db.add(institution)
    db.commit()
    db.refresh(institution)
    return institution

def get_all_branches(db: Session):
    return db.query(InstitutionBranch).all()

def get_institution_by_id(
    db: Session,
    institution_id: int
):
    institution = db.query(InstitutionRegistration).filter(
        InstitutionRegistration.id == institution_id,
        InstitutionRegistration.is_active == True
    ).first()

    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    return institution


# def get_all_branches(db: Session):
#     return db.query(InstitutionBranch).all()


# ======================================================
# INSTITUTION BRANCH SERVICES
# ======================================================

def create_institution_branch(
    db: Session,
    payload: InstitutionBranchCreate
):
    branch = InstitutionBranch(
        **payload.dict(),
        created_date=datetime.utcnow()
    )
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch


def get_branches_by_institution(
    db: Session,
    institution_id: int
):
    return db.query(InstitutionBranch).filter(
        InstitutionBranch.institution_id == institution_id,
        InstitutionBranch.is_active == True
    ).all()

# ======================================================
# STUDENT ACADEMIC DETAILS
# ======================================================

def get_student_full_academic_details(
    db: Session,
    student_id: str = "-1",
    institution_id: int = -1
) -> List[StudentAcademicDetailsSchema]:
    """
    Fetch full student academic details using DB function
    fn_get_student_full_details
    """

    query = text("""
        SELECT *
        FROM fn_get_student_full_details(:student_id, :institution_id)
    """)

    result = db.execute(
        query,
        {
            "student_id": student_id,
            "institution_id": institution_id
        }
    )

    rows = result.mappings().all()

    return [StudentAcademicDetailsSchema(**row) for row in rows]


def create_student_profile(db: Session, payload: StudentProfileCreate):
    existing = db.query(StudentProfile).filter(
        StudentProfile.student_id == payload.student_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, # type: ignore
            detail="Student profile already exists"
        )

    student = StudentProfile(**payload.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_all_students(db: Session):
    return db.query(StudentProfile).filter(
        StudentProfile.is_active == True
    ).all()


def get_active_branch_directory(db: Session, branch_id: int):
    query = text(
        "SELECT * FROM fn_get_branch_directory(:branch_id)"
    )
    result = db.execute(query, {"branch_id": branch_id})
    return result.mappings().all()

def get_student_by_id(db: Session, student_id: int):
    student = db.query(StudentProfile).filter(
        StudentProfile.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student


def update_student_profile(
    db: Session,
    student_id: int,
    payload: StudentProfileUpdate
):
    student = get_student_by_id(db, student_id)

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(student, key, value)

    student.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(student)
    return student


def delete_student_profile(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    student.is_active = False
    student.modified_date = datetime.utcnow()
    db.commit()
    return {"message": "Student profile deactivated successfully"}


# get_students_by_branch service

def fetch_students_by_branch(db, branch_id: int):
    query = text("""
        SELECT * FROM fn_get_students_by_branch(:branch_id)
    """)
    result = db.execute(query, {"branch_id": branch_id})
    return result.mappings().all()   

#ExamSchedule service

from sqlalchemy import text

def create_exam_schedule(db, data):
    query = text("""
        INSERT INTO exam_schedule (
            institution_id,
            exam_type,
            subject_name,
            exam_date,
            start_time,
            end_time,
            location,
            created_by,
            is_active
        )
        VALUES (
            :institution_id,
            :exam_type,
            :subject_name,
            :exam_date,
            :start_time,
            :end_time,
            :location,
            :created_by,
            true
        )
        RETURNING id
    """)

    result = db.execute(query, {
        "institution_id": data.institution_id,
        "exam_type": data.exam_type,
        "subject_name": data.subject_name,
        "exam_date": data.exam_date,
        "start_time": data.start_time,
        "end_time": data.end_time,
        "location": data.location,
        "created_by": data.created_by
    })

    db.commit()
    return result.fetchone()[0]



# Exam List Service
def fetch_exam_schedule(db, exam_type: str, institution_id: int):
    query = text("""
        SELECT * 
        FROM fn_get_exam_schedule(:exam_type, :institution_id)
    """)

    result = db.execute(
        query,
        {
            "exam_type": exam_type,
            "institution_id": institution_id
        }
    )

    return result.mappings().all()





#management

def get_management_overview(
    db: Session,
    institution_id: int,
    academic_year: str
):
    query = text("""
        SELECT * 
        FROM fn_get_management_overview(:institution_id, :academic_year)
    """)

    result = db.execute(
        query,
        {
            "institution_id": institution_id,
            "academic_year": academic_year
        }
        
    )

    return result.mappings().all()

def create_enrollment_status(db: Session,payload: EnrollmentStatusCreate):
    status = EnrollmentStatus(
        **payload.dict(exclude_unset=True),
        created_date=datetime.utcnow(),
        last_updated=datetime.utcnow()
    )
    db.add(status)
    db.commit()
    db.refresh(status)
    return status

def create_bus(db:Session,payload):
    bus = BusFleet(**payload.dict(),created_date = datetime.utcnow())
    db.add(bus)
    db.commit()
    db.refresh(bus)
    return bus

# def get_all_buses(db: Session):
#     return db.query(BusFleet).filter(BusFleet.is_active == True).all()


def create_bus_alert(db: Session, payload: BusAlertCreate):
    alert = BusAlertLog(
        **payload.dict(exclude_unset=True),
        created_date=datetime.utcnow()
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def get_all_alerts(db: Session):
    return db.query(BusAlertLog).filter(
        BusAlertLog.is_active == True
    ).order_by(BusAlertLog.alert_time.desc()).all()

def update_bus_alert(db: Session,alert_id: int,payload: BusAlertUpdate):
    alert = db.query(BusAlertLog).filter(
        BusAlertLog.id == alert_id,
        BusAlertLog.is_active == True
    ).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(alert, key, value)

    alert.modified_date = datetime.utcnow()
    db.commit()
    db.refresh(alert)
    return alert

def get_bus_tracking_overview(db:Session):
    query = text("SELECT * FROM fn_get_bus_tracking_overview()")
    return db.execute(query).mappings().all()

def get_bus_tracking_summary(db:Session):
    query = text("SELECT * FROM fn_get_bus_dashboard_summary()")
    return db.execute(query).mappings().all()

def create_staff_profile(db: Session, payload: StaffProfileCreate):
    staff = StaffProfile(**payload.dict(),created_date=datetime.utcnow())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff

def get_all_staff(db: Session):
    return db.query(StaffProfile).filter(StaffProfile.is_active == True).all()


def create_staff_payslip(db: Session, payload: StaffPayslipCreate):
    payslip = StaffPayslip(**payload.dict(),created_date=datetime.utcnow())
    db.add(payslip)
    db.commit()
    db.refresh(payslip)
    return payslip

def get_payslips_by_staff(db: Session, staff_id: str):
    return db.query(StaffPayslip).filter(
        StaffPayslip.staff_id == staff_id,
        StaffPayslip.is_active == True
    ).all()

def create_payroll_summary(db: Session,payload: PayrollSummaryCreate):
    # check duplicate payroll month
    existing = db.query(PayrollSummary).filter(
        PayrollSummary.payroll_month == payload.payroll_month,
        PayrollSummary.is_active == True
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Payroll summary already exists for this month"
        )

    summary = PayrollSummary(
        **payload.dict(exclude_unset=True),
        created_date=datetime.utcnow()
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary


def get_staff_payslip_summary(db: Session):
    query = text("SELECT * FROM fn_get_staff_payslip_summary()")
    result = db.execute(query).mappings().all()
    return result

def create_maintenance_budget_service(
    payload: MaintenanceBudgetCreate,
    db: Session
):
    budget = MaintenanceBudget(
        institute_id=payload.institute_id,
        budget_limit=payload.budget_limit,
        budget_used=payload.budget_used,
        status=payload.status,
        created_by=payload.created_by
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget
