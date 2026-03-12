from decimal import Decimal

from pydantic import BaseModel, EmailStr, field_validator
from typing import Dict, Optional
from datetime import date, datetime

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import mapped_column


class PartnerUserCreate(BaseModel):
    email: str
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class PartnerUserResponse(BaseModel):
    id: int
    email: str
    created_date: Optional[datetime]

    class Config:
        from_attributes = True


# -------------------------
# Partner Registration
# -------------------------


class PartnerRegistrationCreate(BaseModel):
    module_id: int
    service_module_category_id: int
    user_id: int


class PartnerRegistrationResponse(PartnerRegistrationCreate):
    id: int

    class Config:
        from_attributes = True


# -------------------------
# General Education
# -------------------------


class GeneralEducationCreate(BaseModel):

    partner_registration_id: int
    name: str
    registration_type_id: int
    pan_number: str
    upload_fire_safety_certificate: str
    address_pincode: str
    official_email: str
    gst_registration: Optional[bool] = None
    upload_gst_certificate: Optional[str] = None
    bank_account: Optional[str] = None
    trade_license: Optional[bool] = None
    noc: Optional[bool] = None
    building_type_id: Optional[int] = None
    upload_rental_agreement: Optional[str] = None
    phone_number: Optional[str] = None


class GeneralEducationResponse(GeneralEducationCreate):

    id: int

    class Config:
        from_attributes = True


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
    job_locations: dict
    no_of_vacancies: int
    salary_ctc_range: str
    application_deadline: date
    minimun_education_id: int
    department_ministry_name: str
    pay_scale: Decimal
    selection_process: str
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

class HospitalRegistrationCreate(BaseModel):

    partner_registration_id: int
    hospital_name: str
    upload_entity_photo: str
    hospital_type_id: int
    bed_capacity: int
    management_type_id: int
    establishment_year: int
    address: str
    city: str
    state: str
    pincode: int
    registration_number: str
    doctor_registration: str
    official_email: str
    primary_phone_number: str
    medical_superintendent_name: str
    medical_superintendent_contact: str
    official_mobile_for_otp: str
    official_email_for_otp: str
    created_by: int


class LabRegistrationCreate(BaseModel):

    partner_registration_id: int
    lab_name: str
    upload_entity_photo: str
    lab_type_id: int
    services_offered: Dict
    establishment_year: int
    address: str
    city: str
    state: str
    pincode: int
    registration_number: str
    doctor_registration: str

    upload_registration_certificate: str
    upload_owner_id_proof: str
    upload_owner_address_proof: str
    upload_doctor_registration: str
    upload_labs_equipment_calibration_reports: str

    official_email: str
    primary_phone_number: str
    lab_in_charge_name: str
    lab_in_charge_contact: str

    official_mobile_for_otp: str
    official_email_for_otp: str

    drug_license_applicable: Optional[bool] = False
    drug_license_number: Optional[str] = None

    bmw_obtained: Optional[bool] = False
    bmw_authorization_number: Optional[str] = None

    cbwtf_tied_up: Optional[bool] = False
    cbwtf_facility_name: Optional[str] = None

    fire_noc_obtained: Optional[bool] = False
    fire_noc_number: Optional[str] = None

    aerb_licence_applicable: Optional[bool] = False
    aerb_license_number: Optional[str] = None

    pcpndt_certificate_applicable: Optional[bool] = False
    pcpndt_certificate_number: Optional[str] = None

    nabl_accreditation: Optional[bool] = False
    gst_registered: Optional[bool] = False
    gst_number: Optional[str] = None

    alternate_phone_number: Optional[str] = None
    website_url: Optional[str] = None
    home_sample_collection_available: Optional[bool] = None

    created_by: Optional[int] = None

class MedicalStoreRegistrationCreate(BaseModel):

    partner_registration_id: int
    medical_store_name: str
    upload_entity_photo: str
    store_type_id: int
    establishment_year: int
    address: str
    city: str
    state: str
    pincode: int
    registration_number: str
    pharmacist_registration: str

    upload_registration_certificate: str
    upload_owner_id_proof: str
    upload_owner_address_proof: str
    upload_pharmacist_registration_certificate: str
    upload_shop_registration: str

    official_email: str
    primary_phone_number: str
    pharmacist_owner_name: str
    pharmacist_contact: str

    official_mobile_for_otp: str
    official_email_for_otp: str

    is_24hours_operation: Optional[bool] = None
    home_delivery_available: Optional[bool] = None
    drug_license_applicable: Optional[bool] = None
    fire_noc_obtained: Optional[bool] = None
    gst_registered: Optional[bool] = None

    alternate_phone_number: Optional[str] = None
    website_url: Optional[str] = None

    created_by: int

class MedicalStoreRegistrationResponse(MedicalStoreRegistrationCreate):
    id: int
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True


# ---------------- DOCTOR ----------------
class DoctorRegistrationCreate(BaseModel):
    partner_registration_id: int
    doctor_clinic_name: str
    upload_clinic_photo: str
    doctor_name: str
    specialization: str
    qualification: str
    experience_years: int
    practice_type_id: int
    establishment_year: int
    address: str
    city: str
    state: str
    pincode: int
    registration_number: str
    doctor_registration: str
    upload_registration_certificate: str
    upload_owner_id_proof: str
    upload_owner_address_proof: str
    upload_doctor_registration: str
    upload_medical_degree_certificate: str
    upload_specialization_certificate: str
    official_email: EmailStr
    primary_phone_number: str
    consultation_timings: str
    official_mobile_for_otp: str
    official_email_for_otp: str
    created_by: int


class DoctorRegistrationResponse(DoctorRegistrationCreate):
    id: int
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True


class MyFoodRegistrationCreate(BaseModel):

    partner_registration_id: int
    restaurant_name: str
    restaurant_photo: str
    establishment_year: int
    cuisine_type: Dict
    seating_capacity: int
    owner_name: str
    owner_phone_number: str
    business_registration_number: str
    special_menu_items: Dict
    average_price_per_meal: Decimal
    operating_hours: str

    upload_menu_card: str
    upload_business_registration_certificate: str
    upload_fssai_license_certificate: str
    upload_gst_certificate: str
    upload_owner_id_proof: str
    upload_owner_address_proof: str
    upload_food_license_certificate: str
    upload_health_inspection_report: str
    upload_fire_noc_certificate: str

    manager_name: Optional[str] = None
    manager_phone_number: Optional[str] = None

    fssai_license_registered: Optional[bool] = None
    fssai_license_number: Optional[str] = None

    gst_registered: Optional[bool] = None
    gst_number: Optional[str] = None

    food_license_applicable: Optional[bool] = None
    food_license_number: Optional[str] = None

    health_safety_certfied: Optional[bool] = None
    health_inspection_certifiate_number: Optional[str] = None

    fire_noc_certficate: Optional[bool] = None
    fire_noc_number: Optional[str] = None

    avialable_dining_options: Optional[Dict] = None

    created_by: int


class MyFoodRegistrationResponse(MyFoodRegistrationCreate):
    id: int
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True
