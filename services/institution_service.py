from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException,status

from models.generated_models import (
    BusAlertLog,
    BusFleet,
    EnrollmentStatus,
    EnrollmentStatus,
    ExamInvigilationAssignment,
    ExamNotificationLog,
    ExamReminderSettings,
    InstitutionRegistration,
    InstitutionBranch,
    MaintenanceBudget,
    PayrollPeriod,
    PayrollSummary,
    SalaryEarnings,
    StaffPayslip,
    StaffProfile,
    StudentFeeInstallments,
    StudentProfile,
    StudentSemAcademicProgress
)
from sqlalchemy import text
from typing import List
from schemas.institution_schema import (
    BusAlertCreate,
    BusAlertUpdate,
    EnrollmentStatusCreate,
    ExamInvigilationAssignmentCreate,
    ExamInvigilationAssignmentUpdate,
    ExamNotificationCreate,
    ExamNotificationUpdate,
    ExamReminderCreate,
    InstitutionRegistrationCreate,
    InstitutionBranchCreate,
    MaintenanceBudgetCreate,
    PayrollPeriodCreate,
    PayrollSummaryCreate,
    SalaryEarningsCreate,
    StaffPayslipCreate,
    StaffProfileCreate,
    StudentAcademicDetailsSchema,
    StudentFeeInstallmentCreateSchema,
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentSemAcademicProgressCreate,
    
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

def get_bus_fleet(db: Session):
    query = text("""
        SELECT *
        FROM bus_fleet
        WHERE is_active = true
    """)
    return db.execute(query).mappings().all()




#management

# def get_management_overview(
#     db: Session,
#     institution_id: int,
#     academic_year: str
# ):
#     query = text("""
#         SELECT * 
#         FROM fn_get_management_overview(:institution_id, :academic_year)
#     """)

#     result = db.execute(
#         query,
#         {
#             "institution_id": institution_id,
#             "academic_year": academic_year
#         }
        
#     )

#     return result.mappings().all()
def get_management_overview(
    db: Session,
    institution_id: int | None = None,
    academic_year: str | None = None
):
    query = text("""
        SELECT *
        FROM public.fn_get_management_overview(:institution_id, :academic_year)
    """)

    params = {
        "institution_id": institution_id if institution_id is not None else -1,
        "academic_year": academic_year if academic_year is not None else "-1"
    }

    result = db.execute(query, params)

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



def create_exam_notification(
    db: Session,
    payload: ExamNotificationCreate
):
    notification = ExamNotificationLog(
        **payload.dict(exclude_unset=True),
        created_date=datetime.utcnow()
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_exam_notifications_by_schedule(
    db: Session,
    exam_schedule_id: int
):
    return db.query(ExamNotificationLog).filter(
        ExamNotificationLog.exam_schedule_id == exam_schedule_id,
        ExamNotificationLog.is_active == True
    ).order_by(
        ExamNotificationLog.created_date.desc()
    ).all()


def update_exam_notification(
    db: Session,
    notification_id: int,
    payload: ExamNotificationUpdate
):
    notification = db.query(ExamNotificationLog).filter(
        ExamNotificationLog.id == notification_id,
        ExamNotificationLog.is_active == True
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(notification, key, value)

    notification.modified_date = datetime.utcnow()
    db.commit()
    db.refresh(notification)
    return notification

def get_exam_notification_by_id(
    db: Session,
    notification_id: int
):
    notification = db.query(ExamNotificationLog).filter(
        ExamNotificationLog.id == notification_id,
        ExamNotificationLog.is_active == True
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Exam notification not found"
        )

    return notification

#payroll period

def create_payroll_period(db: Session, data: PayrollPeriodCreate):
    payroll_period = PayrollPeriod(
        month=data.month,
        year=data.year,
        start_date=data.start_date,
        end_date=data.end_date,
        created_by=data.created_by,
        is_active=True
    )

    db.add(payroll_period)
    db.commit()
    db.refresh(payroll_period)  # fetch id, created_date from DB

    return payroll_period


def create_exam_reminder_service(db: Session, payload: ExamReminderCreate):

    reminder = ExamReminderSettings(
        exam_schedule_id=payload.exam_schedule_id,
        enable_notifications=payload.enable_notifications,
        trigger_time=payload.trigger_time,
        notification_sound=payload.notification_sound,
        created_by=payload.created_by,
        is_active=payload.is_active,
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return reminder


def get_all_exam_reminders_service(db: Session):

    reminders = db.query(ExamReminderSettings).filter(
        ExamReminderSettings.is_active == True
    ).all()

    if not reminders:
        raise HTTPException(status_code=404, detail="No reminders found")

    return reminders



def create_exam_invigilation_assignment(
    db: Session,
    payload: ExamInvigilationAssignmentCreate
):
    assignment = ExamInvigilationAssignment(**payload.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def get_all_exam_invigilation_assignments(db: Session):
    return db.query(ExamInvigilationAssignment).filter(
        ExamInvigilationAssignment.is_active == True
    ).all()


def get_exam_invigilation_assignment_by_id(
    db: Session,
    assignment_id: int
):
    assignment = db.query(ExamInvigilationAssignment).filter(
        ExamInvigilationAssignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Invigilation assignment not found")

    return assignment


def update_exam_invigilation_assignment(
    db: Session,
    assignment_id: int,
    payload: ExamInvigilationAssignmentUpdate
):
    assignment = get_exam_invigilation_assignment_by_id(db, assignment_id)

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(assignment, key, value)

    assignment.modified_date = datetime.utcnow()
    db.commit()
    db.refresh(assignment)
    return assignment


def delete_exam_invigilation_assignment(
    db: Session,
    assignment_id: int
):
    assignment = get_exam_invigilation_assignment_by_id(db, assignment_id)
    assignment.is_active = False
    assignment.modified_date = datetime.utcnow()
    db.commit()
    return {"message": "Exam invigilation assignment deactivated"}




def get_salary_summary_service(
    db: Session,
    year: int | None = None,
    month: str | None = None,
    status: str | None = None,
):
    query = text("""
        SELECT *
        FROM vw_salary_summary
        WHERE
            (:year IS NULL OR year = :year)
        AND (:month IS NULL OR month = :month)
        AND (:status IS NULL OR status = :status)
        ORDER BY year DESC, payroll_period_id DESC
    """)

    return db.execute(
        query,
        {
            "year": year,
            "month": month,
            "status": status,
        }
    ).mappings().all()
# salary earnings 

def create_salary_earnings(db: Session, data: SalaryEarningsCreate):
    earnings = SalaryEarnings(
        payroll_period_id=data.payroll_period_id,
        total_net_disbursement=data.total_net_disbursement,
        total_deduction=data.total_deduction,
        staff_count=data.staff_count,
        status=data.status,

        basic_salary=data.basic_salary,
        hra=data.hra,
        medical=data.medical,
        conveyance=data.conveyance,
        gross_earnings=data.gross_earnings,

        pf=data.pf,
        professional_tax=data.professional_tax,
        insurance=data.insurance,

        created_by=data.created_by,
        is_active=True
    )

    db.add(earnings)
    db.commit()
    db.refresh(earnings)

    return earnings


def get_student_full_details_service(
    db: Session,
    student_id: str,
    branch_id: int
):
    query = text("""
        SELECT *
        FROM fn_get_student_full_details(:student_id, :branch_id)
    """)

    return db.execute(
        query,
        {
            "student_id": student_id,
            "branch_id": branch_id
        }
    ).mappings().all()

def create_student_fee_installment(
    db: Session,
    data: StudentFeeInstallmentCreateSchema
):
    # Check duplicate installment
    existing = db.query(StudentFeeInstallments).filter(
        StudentFeeInstallments.student_id == data.student_id,
        StudentFeeInstallments.installment_no == data.installment_no,
        StudentFeeInstallments.is_active == True
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Installment already exists for this student"
        )

    installment = StudentFeeInstallments(
        student_id=data.student_id,
        installment_no=data.installment_no,
        installment_amount=data.installment_amount,
        due_date=data.due_date,
        paid_date=data.paid_date,
        academic_year=data.academic_year,
        is_active=True
    )

    db.add(installment)
    db.commit()
    db.refresh(installment)

    return installment

def get_student_fee_installments(
    db: Session,
    student_id: str
):
    data = db.query(StudentFeeInstallments).filter(
        StudentFeeInstallments.student_id == student_id,
        StudentFeeInstallments.is_active == True
    ).order_by(StudentFeeInstallments.installment_no).all()

    if not data:
        raise HTTPException(
            status_code=404,
            detail="No fee installments found for this student"
        )

    return data


#post student_sem_academic_progress
def create_student_sem_academic_progress(
    db: Session,
    data: StudentSemAcademicProgressCreate
):
    record = StudentSemAcademicProgress(
        student_id=data.student_id,
        academic_year=data.academic_year,
        semester_no=data.semester_no,
        sgpa=data.sgpa,
        attendance_percent=data.attendance_percent,
        backlogs=data.backlogs,
        created_by=data.created_by,
        is_active=True
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record





# ---------- GET BY STUDENT ID ----------
def get_student_sem_academic_progress_by_student_id(
    db: Session,
    student_id: str
):
    return (
        db.query(StudentSemAcademicProgress)
        .filter(
            StudentSemAcademicProgress.student_id == student_id,
            StudentSemAcademicProgress.is_active == True
        )
        .all()
    )

