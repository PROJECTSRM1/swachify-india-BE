



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
    MaintenanceBudgetCreate,
    MaintenanceBudgetResponse,
    PayrollSummaryCreate,
    PayrollSummaryResponse,
    StaffPayslipCreate,
    StaffPayslipResponse,
    StaffProfileCreate,
    StaffProfileResponse
)
from services.institution_service import (
    create_bus,
    create_bus_alert,
    create_enrollment_status,
    create_maintenance_budget_service,
    create_maintenance_budget_service,
    create_payroll_summary,
    create_staff_payslip,
    create_staff_profile,
    get_all_alerts,
    get_all_staff,
    get_all_staff,
    get_bus_fleet,
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

@router.get(
    "/bus-fleet/get-all-buses",
    response_model=list[BusFleetResponse]
)
def get_bus_fleet_api(db: Session = Depends(get_db)):
    return get_bus_fleet(db)
