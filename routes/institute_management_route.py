



from email.mime import text
from fastapi import APIRouter, Depends, Path
from fastapi.params import Query
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.institution_schema import (
    BusFleetCreate,
    BusFleetResponse,
    BusAlertCreate,
    BusAlertResponse,
    BusAlertUpdate,
    EnrollmentStatusCreate,
    EnrollmentStatusResponse,
    ExamInvigilationAssignmentCreate,
    ExamInvigilationAssignmentResponse,
    ExamNotificationCreate,
    ExamNotificationResponse,
    ExamReminderCreate,
    ExamReminderResponse,
    ExamScheduleCreate,
    MaintenanceBudgetCreate,
    MaintenanceBudgetResponse,
    PayrollPeriodCreate,
    PayrollPeriodResponse,
    PayrollSummaryCreate,
    PayrollSummaryResponse,
    SalaryEarningsCreate,
    SalaryEarningsResponse,
    StaffPayslipCreate,
    StaffPayslipResponse,
    StaffProfileCreate,
    StaffProfileResponse
)
from services.institution_service import (
    create_bus,
    create_bus_alert,
    create_enrollment_status,
    create_exam_invigilation_assignment,
    create_exam_notification,
    create_exam_reminder_service,
    create_exam_schedule,
    create_maintenance_budget_service,
    create_maintenance_budget_service,
    create_payroll_period,
    create_payroll_summary,
    create_salary_earnings,
    create_staff_payslip,
    create_staff_profile,
    fetch_exam_schedule,
    get_all_alerts,
    get_all_exam_reminders_service,
    get_all_staff,
    get_all_staff,
    get_bus_fleet,
    get_exam_invigilation_assignment_by_id,
    get_salary_summary_service,
    get_staff_payslip_summary,
    get_bus_fleet,
    get_exam_notification_by_id,
    get_management_overview,
    get_payslips_by_staff,
    get_staff_payslip_summary,
    update_bus_alert,
    get_bus_tracking_overview,
    get_bus_tracking_summary
)

router = APIRouter(prefix="/institution/management",tags=["Institution Management"])

@router.get("/management-overview")
def management_overview_api(
    institution_id: int = Query(
        -1,
        description="Pass institution_id or -1 for all institutions"
    ),
    academic_year: str = Query(
        "-1",
        description="Pass academic year (e.g. 2023-2024) or -1 for all"
    ),
    db: Session = Depends(get_db)
):
    return get_management_overview(
        db,
        institution_id,
        academic_year
    )


@router.post("/enrollment-status/create",response_model=EnrollmentStatusResponse)
def create_enrollment_status_api(payload: EnrollmentStatusCreate,db: Session = Depends(get_db)):
    return create_enrollment_status(db, payload)

@router.post("/bus/create", response_model=BusFleetResponse)
def create_bus_api(payload: BusFleetCreate,db: Session = Depends(get_db)):
    return create_bus(db, payload)

# @router.get("/bus/all", response_model=list[BusFleetResponse])
# def get_all_buses_api(db: Session = Depends(get_db)):
#     return get_all_buses(db)

@router.post("/bus/alerts",response_model=BusAlertResponse)
def create_bus_alert_api(payload: BusAlertCreate,db: Session = Depends(get_db)):
    return create_bus_alert(db, payload)


@router.get("/bus/alerts",response_model=list[BusAlertResponse])
def get_all_alerts_api(db: Session = Depends(get_db)):
    return get_all_alerts(db)

@router.put("/bus/{alert_id}",response_model=BusAlertResponse)
def update_bus_alert_api(alert_id: int = Path(..., gt=0),payload: BusAlertUpdate = None,db: Session = Depends(get_db)):
    return update_bus_alert(db, alert_id, payload)

@router.get("/bus-tracking-overview")
def bus_tracking_overview(db:Session = Depends(get_db)):
    return get_bus_tracking_overview(db)

@router.get("/bus-tracking-summary")
def bus_tracking_summary(db:Session = Depends(get_db)):
    return get_bus_tracking_summary(db)

@router.post("/staff-profile/create",response_model=StaffProfileResponse)
def create_staff_api(payload: StaffProfileCreate,db: Session = Depends(get_db)):
    return create_staff_profile(db, payload)

@router.get("/staff-profile/all",response_model=list[StaffProfileResponse])
def get_all_staff_api(db: Session = Depends(get_db)):
    return get_all_staff(db)

@router.post("/payslip/create",response_model=StaffPayslipResponse)
def create_payslip_api(payload: StaffPayslipCreate,db: Session = Depends(get_db)):
    return create_staff_payslip(db, payload)

@router.get("/{staff_id}/payslips",response_model=list[StaffPayslipResponse])
def get_payslips_by_staff_api(staff_id: str,db: Session = Depends(get_db)):
    return get_payslips_by_staff(db, staff_id)

# @router.post("/payslips/summary",response_model=PayrollSummaryResponse)
# def create_payroll_summary_api(payload: PayrollSummaryCreate,db: Session = Depends(get_db)):
#     return create_payroll_summary(db, payload)


@router.get("/payslip-summary")
def fetch_staff_payslip_summary(db: Session = Depends(get_db)):
    return get_staff_payslip_summary(db)




@router.post("/maintenance_budget", response_model=MaintenanceBudgetResponse)
def create_maintenance_budget(payload: MaintenanceBudgetCreate,db: Session = Depends(get_db)):
    return create_maintenance_budget_service(payload, db)


#exam schedule route
@router.post("/exam-schedule")
def create_exam(payload: ExamScheduleCreate,db: Session = Depends(get_db)):
    exam_id = create_exam_schedule(db, payload)
    return {
        "message": "Exam schedule created successfully",
        "exam_schedule_id": exam_id
    }


@router.get("/exam-schedule")
def get_exam_schedule(
    exam_type: str = "-1",
    institution_id: int = -1,
    db: Session = Depends(get_db)
):
    return fetch_exam_schedule(db, exam_type, institution_id)




@router.post(
    "/exam-notification",
    response_model=ExamNotificationResponse
)
def create_exam_notification_api(
    payload: ExamNotificationCreate,
    db: Session = Depends(get_db)
):
    return create_exam_notification(db, payload)

@router.get(
    "/exam-notification/id/{notification_id}",
    response_model=ExamNotificationResponse
)
def get_exam_notification_by_id_api(
    notification_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    return get_exam_notification_by_id(db, notification_id)




@router.post("/ Create-Exam-Reminder", response_model=ExamReminderResponse)
def create_exam_reminder(
    payload: ExamReminderCreate,
    db: Session = Depends(get_db)
):
    return create_exam_reminder_service(db, payload)


@router.get("/Get-All-Exam-Reminder", response_model=list[ExamReminderResponse])
def get_all_exam_reminders(
    db: Session = Depends(get_db)
):
    return get_all_exam_reminders_service(db)


@router.post(
    "/exam-invigilation",
    response_model=ExamInvigilationAssignmentResponse
)
def create_exam_invigilation_api(
    payload: ExamInvigilationAssignmentCreate,
    db: Session = Depends(get_db)
):
    return create_exam_invigilation_assignment(db, payload)

@router.get(
    "exam-invigilation/{assignment_id}",
    response_model=ExamInvigilationAssignmentResponse
)
def get_assignment(
    assignment_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    return get_exam_invigilation_assignment_by_id(db, assignment_id)


@router.get(
    "/bus-fleet/get-all-buses",
    response_model=list[BusFleetResponse]
)
def get_bus_fleet_api(db: Session = Depends(get_db)):
    return get_bus_fleet(db)


@router.post(
    "/payroll-period",
    response_model=PayrollPeriodResponse
)
def create_payroll_period_api(
    payload: PayrollPeriodCreate,
    db: Session = Depends(get_db)
):
    return create_payroll_period(db, payload)


@router.post(
    "/salary-earnings",
    response_model=SalaryEarningsResponse
)
def create_salary_earnings_api(
    payload: SalaryEarningsCreate,
    db: Session = Depends(get_db)
):
    return create_salary_earnings(db, payload)




@router.get("/salary-summary")
def get_salary_summary(
    year: int | None = Query(None),
    month: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return get_salary_summary_service(
        db=db,
        year=year,
        month=month,
        status=status,
    )
