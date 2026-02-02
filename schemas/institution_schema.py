from pydantic import BaseModel
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime, time
from decimal import Decimal

# ======================================================
# INSTITUTION REGISTRATION
# ======================================================

class InstitutionRegistrationCreate(BaseModel):
    institution_name: str
    institution_type_id: int
    identity_type_id: int
    identity_number: str
    location: str
    representative_name: str
    email: EmailStr
    phone_number: str

    upload_id_proof: Optional[str] = None
    upload_address_proof: Optional[str] = None
    institute_website: Optional[str] = None
    total_branches: Optional[int] = None
    academic_year_start: Optional[date] = None
    academic_year_end: Optional[date] = None
    created_by: Optional[int] = None
    is_active: Optional[bool] = True

class InstitutionRegistrationResponse(BaseModel):
    id: int

    institution_name: str
    institution_type_id: int
    identity_type_id: int
    identity_number: str
    location: str
    representative_name: str
    email: EmailStr
    phone_number: str

    upload_id_proof: Optional[str] = None
    upload_address_proof: Optional[str] = None
    institute_website: Optional[str] = None
    total_branches: Optional[int] = None
    academic_year_start: Optional[date] = None
    academic_year_end: Optional[date] = None

    created_by: Optional[int] = None
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


# ======================================================
# INSTITUTION BRANCH
# ======================================================

class InstitutionBranchCreate(BaseModel):
    institution_id: int
    branch_name: str
    city: str
    branch_code: str
    branch_head: str
    is_active: Optional[bool] = True


class InstitutionBranchResponse(BaseModel):
    id: int
    institution_id: int
    branch_name: str
    city: str
    branch_code: str
    branch_head: str
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class StudentAcademicDetailsSchema(BaseModel):
    # DB returns this as string (CSE2024_044)
    student_id: str

    # Make everything OPTIONAL unless DB guarantees it
    roll_number: Optional[str] = None

    institution_id: Optional[int] = None
    institution_name: Optional[str] = None

    course_id: Optional[int] = None
    course_name: Optional[str] = None

    department_id: Optional[int] = None
    department_name: Optional[str] = None

    academic_year: Optional[str] = None
    semester: Optional[str] = None

    status: Optional[str] = None

    # Any extra DB columns you saw in error
    paid_date: Optional[date] = None



class StudentProfileBase(BaseModel):
    branch_id: int
    branch_name: str
    student_name: str
    student_id: str
    academic_year: str
    profile_image_url: Optional[str] = None
    is_active: Optional[bool] = True


class StudentProfileCreate(StudentProfileBase):
    created_by: Optional[int] = None


class StudentProfileUpdate(BaseModel):
    branch_id: Optional[int] = None
    branch_name: Optional[str] = None
    student_name: Optional[str] = None
    academic_year: Optional[str] = None
    profile_image_url: Optional[str] = None
    modified_by: Optional[int] = None
    is_active: Optional[bool] = None


class StudentProfileResponse(StudentProfileBase):
    id: int
    branch_id: Optional[int] = None
    branch_name: Optional[str] = None
    student_name: Optional[str] = None
    academic_year: Optional[str] = None
    profile_image_url: Optional[str] = None
    modified_by: Optional[int] = None
    is_active: Optional[bool] = None
    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]

    class Config:
        from_attributes = True
# get_students_by_branch Schema
class StudentResponse(BaseModel):
    student_id: int
    student_code: str
    student_name: str
    year: int
    profile_image: str | None

#ExamSchedule
class ExamScheduleCreate(BaseModel):
    institution_id: int
    exam_type: str
    subject_name: str
    exam_date: date
    start_time: time
    end_time: time
    location: str
    created_by: int



class EnrollmentStatusCreate(BaseModel):
    institute_id: int
    total_capacity: int
    approved_seats: int
    created_by: Optional[int] = None
    is_active: Optional[bool] = True

class EnrollmentStatusResponse(BaseModel):
    id: int
    institute_id: int
    total_capacity: int
    approved_seats: int
    last_updated: datetime
    is_active: bool

    class Config:
        from_attributes = True

class BusFleetCreate(BaseModel):
    bus_id: int 
    bus_name: Optional[str] = None
    driver_name: Optional[str] = None
    created_by: Optional[int] = None
    is_active: Optional[bool] = True

class BusFleetResponse(BaseModel):
    id: int
    bus_id: str
    bus_name: Optional[str]
    driver_name: Optional[str]
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class BusAlertCreate(BaseModel):
    bus_id: int
    alert_type: Optional[str] = None
    alert_message: Optional[str] = None
    created_by: Optional[int] = None
    is_active: Optional[bool] = True

class BusAlertUpdate(BaseModel):
    alert_type: Optional[str] = None
    alert_message: Optional[str] = None
    resolved: Optional[bool] = None
    modified_by: Optional[int] = None
    is_active: Optional[bool] = None

class BusAlertResponse(BaseModel):
    id: int
    bus_id: int
    alert_type: Optional[str]
    alert_message: Optional[str]
    alert_time: datetime
    resolved: bool
    is_active: bool

    class Config:
        from_attributes = True



class StaffProfileCreate(BaseModel):
    staff_id: int
    staff_name: str
    job_title: Optional[str] = None
    department: Optional[str] = None
    created_by: Optional[int] = None
    is_active: Optional[bool] = True


class StaffProfileResponse(BaseModel):
    id: int
    staff_id: str
    staff_name: str
    job_title: Optional[str]
    department: Optional[str]
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class StaffPayslipCreate(BaseModel):
    staff_id: int
    payroll_month: str
    payment_date: Optional[date] = None

    basic_pay: Optional[Decimal] = None
    hra: Optional[Decimal] = None
    medical_allowance: Optional[Decimal] = None
    conveyance: Optional[Decimal] = None
    performance_bonus: Optional[Decimal] = None

    gross_earnings: Optional[Decimal] = None
    pf_deduction: Optional[Decimal] = None
    income_tax: Optional[Decimal] = None
    professional_tax: Optional[Decimal] = None
    health_insurance: Optional[Decimal] = None

    total_deductions: Optional[Decimal] = None
    net_salary: Optional[Decimal] = None

    created_by: Optional[int] = None
    is_active: Optional[bool] = True


class StaffPayslipResponse(BaseModel):
    id: int
    staff_id: str
    payroll_month: str
    payment_date: Optional[date]

    basic_pay: Optional[Decimal]
    hra: Optional[Decimal]
    medical_allowance: Optional[Decimal]
    conveyance: Optional[Decimal]
    performance_bonus: Optional[Decimal]

    gross_earnings: Optional[Decimal]
    pf_deduction: Optional[Decimal]
    income_tax: Optional[Decimal]
    professional_tax: Optional[Decimal]
    health_insurance: Optional[Decimal]

    total_deductions: Optional[Decimal]
    net_salary: Optional[Decimal]

    status: Optional[str]
    created_by: Optional[int]
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True

class PayrollSummaryCreate(BaseModel):
    payroll_month: str
    total_net_disbursement: Optional[Decimal] = None
    staff_count: Optional[int] = None
    status: Optional[str] = "DISBURSED"
    created_by: Optional[int] = None
    is_active: Optional[bool] = True


class PayrollSummaryResponse(BaseModel):
    id: int
    payroll_month: str
    total_net_disbursement: Optional[Decimal]
    staff_count: Optional[int]
    status: Optional[str]
    created_by: Optional[int]
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True

class MaintenanceBudgetCreate(BaseModel):
    institute_id: int
    budget_limit: Optional[Decimal] = None
    budget_used: Optional[Decimal] = None
    status: Optional[str] = None
    created_by: Optional[int] = None

class MaintenanceBudgetResponse(BaseModel):
    id: int
    institute_id: int
    budget_limit: Optional[Decimal]
    budget_used: Optional[Decimal]
    status: Optional[str]
    created_by: Optional[int]
    created_date: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True



class ExamNotificationCreate(BaseModel):
    exam_schedule_id: int
    message: Optional[str] = None
    scheduled_date: Optional[date] = None
    created_by: Optional[int] = None
    is_active: Optional[bool] = True


class ExamNotificationUpdate(BaseModel):
    message: Optional[str] = None
    sent_count: Optional[int] = None
    failed_count: Optional[int] = None
    retry_success: Optional[int] = None
    status: Optional[str] = None
    modified_by: Optional[int] = None
    is_active: Optional[bool] = None


class ExamNotificationResponse(BaseModel):
    id: int
    exam_schedule_id: int
    message: Optional[str]
    sent_count: Optional[int]
    failed_count: Optional[int]
    retry_success: Optional[int]
    scheduled_date: Optional[date]
    status: Optional[str]
    created_by: Optional[int]
    created_date: datetime
    modified_by: Optional[int]
    modified_date: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True