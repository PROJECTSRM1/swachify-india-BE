from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional, List, Any, Dict
from datetime import date, datetime
from decimal import Decimal

from schemas.student_family_schema import StudentFamilyMemberResponse

# =====================================================
# JOB OPENINGS
# =====================================================

class JobOpeningCreate(BaseModel):
    job_id: int
    company_name: str
    company_address: Optional[str] = None

    industry_id: Optional[int] = None        # ✅ ADD
    company_size_id: Optional[int] = None    # ✅ ADD

    location_type_id: Optional[int] = None
    work_type_id: Optional[int] = None
    role_description: Optional[str] = None
    requirements: Optional[str] = None
    sub_module_id: Optional[int] = None


class JobOpeningResponse(BaseModel):
    id: int
    job_id: int
    company_name: str
    company_address: Optional[str] = None
    industry_id: Optional[int] = None          # ✅ ADD
    company_size_id: Optional[int] = None      # ✅ ADD

    location_type_id: Optional[int] = None
    work_type_id: Optional[int] = None
    role_description: Optional[str] = None
    requirements: Optional[str] = None
    is_active: bool
    created_date: Optional[datetime]

    class Config:
        from_attributes = True


# =====================================================
# JOB APPLICATION
# =====================================================

class JobApplicationCreate(BaseModel):
    job_openings_id: int
    first_name: str
    last_name: str
    mobile_number: str
    mobile_code_id: int
    email: EmailStr
    city_id: int

    upload_resume: str
    notice_period_in_days: int

    fresher: bool
    experienced: bool

    company: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    company_city_id: Optional[int] = None
    current_ctc: Optional[Decimal] = None
    expected_ctc: Optional[Decimal] = None
    title: Optional[str] = None
    description: Optional[str] = None

    @model_validator(mode="after")
    def validate_fresher_vs_experienced(self):
        if self.fresher and not self.experienced:
            if any([
                self.company,
                self.from_date,
                self.to_date,
                self.company_city_id,
                self.current_ctc
            ]):
                raise ValueError(
                    "Fresher should not have company, dates, city or CTC"
                )

        elif self.experienced and not self.fresher:
            required = [
                self.company,
                self.from_date,
                self.to_date,
                self.company_city_id,
                self.current_ctc
            ]
            if not all(required):
                raise ValueError(
                    "Experienced candidate must provide company, dates, city and current_ctc"
                )
        else:
            raise ValueError(
                "Either fresher=true or experienced=true (not both)"
            )
        return self


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_openings_id: int

    first_name: str
    last_name: str
    mobile_number: str
    mobile_code_id: int
    email: EmailStr

    city_id: int
    upload_resume: str
    notice_period_in_days: int

    title: Optional[str]
    company: Optional[str]
    from_date: Optional[date]
    to_date: Optional[date]
    company_city_id: Optional[int]
    description: Optional[str]

    current_ctc: Optional[Decimal]
    expected_ctc: Optional[Decimal]

    fresher: Optional[bool]
    experienced: Optional[bool]

    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True


# =====================================================
# STUDENT CERTIFICATE
# =====================================================

class StudentCertificateCreate(BaseModel):
    certificate_name: str
    issued_by: str
    year: int
    upload_certificate: Optional[str] = None


class StudentCertificateResponse(BaseModel):
    id: int
    certificate_name: str
    issued_by: Optional[str] = None
    year: Optional[int] = None
    upload_certificate: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True



# =====================================================
# STUDENT EDUCATION
# =====================================================

class StudentEducationCreate(BaseModel):
    degree: str
    institute: str
    percentage: str
    passing_year: Optional[int] = None


class StudentEducationResponse(BaseModel):
    degree: str
    institute: Optional[str] = None
    percentage: Optional[str] = None
    
    class Config:
        from_attributes = True

# =====================================================
# STUDENT NOC
# =====================================================

class StudentNOCUpdate(BaseModel):
    noc_number: str
    police_station_name: str
    issue_year: int
    upload_noc: Optional[str] = None


class StudentNOCResponse(BaseModel):
    noc_number: str
    police_station_name: str
    issue_year: int
    upload_noc: Optional[str]

    class Config:
        from_attributes = True


# =====================================================
# STUDENT PROFILE (BASIC)
# =====================================================

class StudentProfileResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str
    government_id: Any
    location: Optional[str]
    service_name: str
    family_members: List[StudentFamilyMemberResponse] = []
    
    class Config:
        from_attributes = True


# =====================================================
# STUDENT FULL UPDATE (EDU / CERT / NOC)
# =====================================================

class StudentEducationFullCreate(BaseModel):
    education: Optional[List[StudentEducationCreate]] = None
    certificates: Optional[List[StudentCertificateCreate]] = None
    noc: Optional[StudentNOCUpdate] = None

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if not (values.education or values.certificates or values.noc):
            raise ValueError(
                "At least one of education, certificates, or noc must be provided."
            )
        return values


# =====================================================
# STUDENT LIST RESPONSE (NO DUPLICATES)
# =====================================================

class StudentListResponse(BaseModel):
    user_id: int
    student_name: str
    joined_date: Optional[datetime]

    skill_id: Optional[int]
    skill: Optional[str]

    attendance_percentage: Optional[Decimal]
    aggregate: Optional[str]

    internship_status: Optional[str]
    rating: Optional[Decimal]

    education: List[StudentEducationResponse] = []
    certificates: List[StudentCertificateResponse] = []

    class Config:
        from_attributes = True

# # get_students_by_branch Schema
# class StudentResponse(BaseModel):
#     student_id: int
#     student_code: str
#     student_name: str
#     year: int
#     profile_image: str | None


class InstitutionSchoolCollegeRegistrationCreate(BaseModel):

    partner_registration_id: int
    institution_name: str
    establishment_year: int
    management_type_id: int
    country: str
    state: str
    district: str
    city: str
    address: str
    pincode: int
    official_email: str
    official_phone_number: str
    director_principal_name: str
    director_contact_number: str
    registration_number: str
    affiliation_board_university: str
    upload_registration_certificate: str
    upload_affiliation_proof: str
    upload_principal_id_proof: str

    education_medium: Dict
    education_grades_offered: Dict
    student_capacity: int
    current_student_strength: int
    teacher_count: int

    streams_offered: Dict
    degree_courses_offered: Dict

    board_affiliation_id: int
    available_pg_programs: Dict

    institution_type_id: Optional[int] = None
    upload_institution_logo: Optional[str] = None
    website_url: Optional[str] = None
    accreditation: Optional[str] = None
    gst_number: Optional[str] = None

    created_by: int


class StudentRegistrationCreate(BaseModel):

    partner_registration_id: int
    student_name: str
    aadhar_number: str
    mobile_number: str
    email: str
    residential_address: str
    city: str
    state: str
    pincode: int

    highest_qualification_id: int
    school_college_name: str
    board_university: str
    passing_year: int
    cgpa_percentage: Decimal

    study_medium_id: int
    applying_application_interst: Dict
    cast_category_id: int

    upload_profile_photo: str
    upload_aadhar_card: str
    upload_10th_marksheet: str

    date_of_birth: Optional[date] = None
    gender_id: Optional[int] = None

    preferred_institution_course: Optional[str] = None
    preferred_location: Optional[str] = None

    require_scholarship: Optional[bool] = None
    require_hostel_facility: Optional[bool] = None
    require_transport_facility: Optional[bool] = None

    technical_skills: Optional[Dict] = None
    extra_curricular_achievements: Optional[str] = None
    career_objective: Optional[str] = None

    upload_12th_marksheet: Optional[str] = None
    upload_degree_certificate: Optional[str] = None
    upload_resume: Optional[str] = None
    upload_transfer_certificate: Optional[str] = None
    upload_cast_certificate: Optional[str] = None
    upload_income_certificate: Optional[str] = None

    created_by: int

class CompaniesRegistrationCreate(BaseModel):

    partner_registration_id: int
    company_name: str
    company_registration_number: str
    official_email: str
    hr_contact_number: str
    company_hq_address: str

    company_type_id: int
    upload_gst_certificate: str
    job_sector_id: int
    job_title: str
    job_description: str

    job_type_id: int
    work_mode_id: int
    job_locations: Dict

    no_of_vacancies: int
    salary_ctc_range: str
    application_deadline: date

    minimun_education_id: int
    department_ministry_name: str
    pay_scale: Decimal
    selection_process: str

    company_website_url: Optional[str] = None
    upload_company_logo: Optional[str] = None
    required_experience: Optional[str] = None
    minimum_percentage_required: Optional[Decimal] = None
    age_limit: Optional[str] = None

    cast_category_preferences: Optional[Dict] = None
    required_skills: Optional[Dict] = None

    exam_notification_number: Optional[str] = None
    exam_date_announced: Optional[bool] = None
    exam_date: Optional[date] = None

    official_notification_url: Optional[str] = None
    upload_notification_pdf: Optional[str] = None

    tech_stack_category_id: Optional[int] = None
    preferred_tech_stack: Optional[str] = None

    service_agreement_required: Optional[bool] = None
    stock_options_available: Optional[bool] = None

    joining_timeline: Optional[str] = None
    benefits_perks: Optional[Dict] = None

    created_by: int


class TrainingRegistrationCreate(BaseModel):

    partner_registration_id: int
    training_type_id: int
    course_exam_category_id: int
    exam_category_id: int

    institute_provider_name: str
    provider_contact_email: str
    provider_phone_number: str
    provider_location: str

    course_title: str
    course_description: str
    training_mode_id: int
    batch_start_date: date

    language_instruction: Dict
    min_qualification_required_id: int

    upload_course_banner_image: str

    institute_logo: Optional[str] = None
    course_tagline: Optional[str] = None
    course_duration: Optional[str] = None
    total_sessions_hours: Optional[str] = None
    training_fee: Optional[str] = None

    class_schedule_timings: Optional[str] = None
    max_students_per_batch: Optional[int] = None

    course_modules: Optional[Dict] = None
    technologies_covered: Optional[str] = None
    projects_included: Optional[str] = None

    completion_certificate_provided: Optional[bool] = None
    placement_assistance: Optional[bool] = None

    instructor_name_linkedin: Optional[str] = None
    previous_batch_enrolled_count: Optional[int] = None
    previous_batch_pass_percentage: Optional[Decimal] = None

    exam_stages_covered: Optional[Dict] = None
    target_exam_year: Optional[int] = None

    pyq_coverage: Optional[str] = None
    no_of_mock_tests: Optional[int] = None

    study_material_provided: Optional[bool] = None
    current_affairs_coverage: Optional[bool] = None

    past_selection_rank_holders: Optional[str] = None
    hostel_facility: Optional[bool] = None

    upload_sample_study_material: Optional[str] = None
    upload_sample_certificate: Optional[str] = None

    created_by: int