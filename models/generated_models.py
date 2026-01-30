from typing import Optional
import datetime
import decimal

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, ForeignKeyConstraint, Index, Integer, JSON, Numeric, PrimaryKeyConstraint, String, Table, Text, Time, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class MasterAddOn(Base):
    __tablename__ = 'master_add_on'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_add_on_id'),
        UniqueConstraint('add_on', name='uk_master_add_on_add_on')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    add_on: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    hs_add_on: Mapped[list['HsAddOn']] = relationship('HsAddOn', back_populates='add_on')


class MasterAggregate(Base):
    __tablename__ = 'master_aggregate'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_aggregate_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    aggregate: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterApprovalType(Base):
    __tablename__ = 'master_approval_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_approval_type_id'),
        UniqueConstraint('approval_type', name='uk_master_approval_type_approval_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    approval_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterAssistants(Base):
    __tablename__ = 'master_assistants'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_assistants_id'),
        UniqueConstraint('name', name='uk_master_assistants_name')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    rating: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    role: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'Professional'::character varying"))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='assistant')


class MasterAvailabilityStatus(Base):
    __tablename__ = 'master_availability_status'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_availability_status_id'),
        UniqueConstraint('availability_status', name='uk_master_availability_status_availability_status')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    availability_status: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterBathroom(Base):
    __tablename__ = 'master_bathroom'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_bathroom_id'),
        UniqueConstraint('bathroom_count', name='uk_master_bathroom_bathroom_count')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bathroom_count: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterBedroom(Base):
    __tablename__ = 'master_bedroom'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_bedroom_id'),
        UniqueConstraint('bedroom_count', name='uk_master_bedroom_bedroom_count')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bedroom_count: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterBhkType(Base):
    __tablename__ = 'master_bhk_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_bhk_type_id'),
        UniqueConstraint('bhk_type', name='uk_master_bhk_type')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    bhk_type: Mapped[Optional[str]] = mapped_column(String(10))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='bhk_type')


class MasterBoundaryType(Base):
    __tablename__ = 'master_boundary_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_boundary_type_id'),
        UniqueConstraint('boundary_type', name='uk_master_boundary_type_boundary_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    boundary_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterBusinessType(Base):
    __tablename__ = 'master_business_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_business_type_id'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    business_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[list['UserRegistration']] = relationship('UserRegistration', back_populates='business_type')


class MasterCategory(Base):
    __tablename__ = 'master_category'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_master_category_id'),
        UniqueConstraint('category_name', name='uk_master_master_category_category_name')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_openings: Mapped[list['JobOpenings']] = relationship('JobOpenings', back_populates='category')


class MasterCity(Base):
    __tablename__ = 'master_city'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_city_id'),
        UniqueConstraint('city', name='uk_master_city_city')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    city: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_application: Mapped[list['JobApplication']] = relationship('JobApplication', foreign_keys='[JobApplication.city_id]', back_populates='city')
    job_application_: Mapped[list['JobApplication']] = relationship('JobApplication', foreign_keys='[JobApplication.company_city_id]', back_populates='company_city')


class MasterCompanySize(Base):
    __tablename__ = 'master_company_size'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_company_size_id'),
        UniqueConstraint('size_range', name='uk_master_company_size_range')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    size_range: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_openings: Mapped[list['JobOpenings']] = relationship('JobOpenings', back_populates='company_size')


class MasterDepartment(Base):
    __tablename__ = 'master_department'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_department_id'),
        UniqueConstraint('department', name='uk_master_department_department')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    master_designation: Mapped[list['MasterDesignation']] = relationship('MasterDesignation', back_populates='dept')


class MasterDoctorSpecialization(Base):
    __tablename__ = 'master_doctor_specialization'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_doctor_specialization_id'),
        UniqueConstraint('specialization_name', name='uk_master_doctor_specialization_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    specialization_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    doctor_profile: Mapped[list['DoctorProfile']] = relationship('DoctorProfile', back_populates='specialization')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='doctor_specialization')


class MasterDuration(Base):
    __tablename__ = 'master_duration'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_duration_id'),
        UniqueConstraint('duration', name='uk_master_duration_duration')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    duration: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='duration')
    hs_add_on: Mapped[list['HsAddOn']] = relationship('HsAddOn', back_populates='duration')


class MasterFacing(Base):
    __tablename__ = 'master_facing'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_facing_id'),
        UniqueConstraint('facing', name='uk_master_facing_facing')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    facing: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterFuelType(Base):
    __tablename__ = 'master_fuel_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_fuel_type_id'),
        UniqueConstraint('fuel_type_name', name='uk_master_fuel_type_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fuel_type_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    vehicle_brand_fuel: Mapped[list['VehicleBrandFuel']] = relationship('VehicleBrandFuel', back_populates='fuel')
    vehicle_service_booking: Mapped[list['VehicleServiceBooking']] = relationship('VehicleServiceBooking', back_populates='fuel')


class MasterFurnishing(Base):
    __tablename__ = 'master_furnishing'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_furnishing_id'),
        UniqueConstraint('furnisher_type', name='uk_master_furnishig_furnisher_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    furnisher_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='furnishing')


class MasterGender(Base):
    __tablename__ = 'master_gender'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_gender_id'),
        UniqueConstraint('gender_name', name='uk_master_gender_gender_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gender_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[list['UserRegistration']] = relationship('UserRegistration', back_populates='gender')


class MasterHealthCategories(Base):
    __tablename__ = 'master_health_categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_health_categories_id'),
        UniqueConstraint('category_name', name='uk_master_health_categories_category_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterHospital(Base):
    __tablename__ = 'master_hospital'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_hospital_id'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    hospital_name: Mapped[str] = mapped_column(String(255), nullable=False)
    specialty_type: Mapped[Optional[str]] = mapped_column(String(50))
    location: Mapped[Optional[str]] = mapped_column(String(255))
    contact_number: Mapped[Optional[str]] = mapped_column(String(20))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))

    master_ambulance: Mapped[list['MasterAmbulance']] = relationship('MasterAmbulance', back_populates='hospital')


class MasterHostelServices(Base):
    __tablename__ = 'master_hostel_services'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_hostel_services_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_name: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterHostelType(Base):
    __tablename__ = 'master_hostel_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_hostel_type_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hostel_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='hostel_type')


class MasterIdentityType(Base):
    __tablename__ = 'master_identity_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_identity_type_id'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    identity_type_name: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    institution_registration: Mapped[list['InstitutionRegistration']] = relationship('InstitutionRegistration', back_populates='identity_type')


class MasterIndustry(Base):
    __tablename__ = 'master_industry'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_industry_id'),
        UniqueConstraint('industry_name', name='uk_master_industry_name')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    industry_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_openings: Mapped[list['JobOpenings']] = relationship('JobOpenings', back_populates='industry')


class MasterInstituteType(Base):
    __tablename__ = 'master_institute_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_institute_type_id'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    institute_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    institution_registration: Mapped[list['InstitutionRegistration']] = relationship('InstitutionRegistration', back_populates='institution_type')


class MasterInternshipDuration(Base):
    __tablename__ = 'master_internship_duration'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_internship_duration_id'),
        UniqueConstraint('duration_type', name='uk_master_internship_duration_duration_type')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    duration_type: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_openings: Mapped[list['JobOpenings']] = relationship('JobOpenings', back_populates='internship_duration')


class MasterIssue(Base):
    __tablename__ = 'master_issue'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_issue_id'),
        UniqueConstraint('issue_type', name='uk_master_issue_issue_type')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    issue_type: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='issue')


class MasterItemCondition(Base):
    __tablename__ = 'master_item_condition'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_item_condition_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_condition: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='item_condition')


class MasterJob(Base):
    __tablename__ = 'master_job'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_job_id'),
        UniqueConstraint('job_name', name='uk_master_job_job_name')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    job_name: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_openings: Mapped[list['JobOpenings']] = relationship('JobOpenings', back_populates='job')


class MasterJobSkill(Base):
    __tablename__ = 'master_job_skill'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_job_skill_id'),
        UniqueConstraint('skill', name='uk_master_job_skill_skill')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    skill: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[list['UserRegistration']] = relationship('UserRegistration', back_populates='job_skill')


class MasterLabs(Base):
    __tablename__ = 'master_labs'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_master_labs_rating'),
        PrimaryKeyConstraint('id', name='pk_master_labs_id'),
        UniqueConstraint('lab_name', name='master_labs_lab_name_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    lab_name: Mapped[str] = mapped_column(String(255), nullable=False)
    services: Mapped[Optional[str]] = mapped_column(String(255))
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    home_collection: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))

    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='labs')


class MasterLandType(Base):
    __tablename__ = 'master_land_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_land_type_id'),
        UniqueConstraint('land_type', name='uk_master_land_type_land_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    land_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterLeaseType(Base):
    __tablename__ = 'master_lease_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_lease_type_id'),
        UniqueConstraint('lease_type', name='uk_master_lease_type_lease_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lease_type: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterListingType(Base):
    __tablename__ = 'master_listing_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_listing_type_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='listing_type')


class MasterLocationType(Base):
    __tablename__ = 'master_location_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_location_type_id'),
        UniqueConstraint('location_type', name='uk_master_location_type_location_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_openings: Mapped[list['JobOpenings']] = relationship('JobOpenings', back_populates='location_type')


class MasterMobileCode(Base):
    __tablename__ = 'master_mobile_code'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_mobile_code_id'),
        UniqueConstraint('mobile_code', name='uk_master_mobile_code_mobile_code')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    mobile_code: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_application: Mapped[list['JobApplication']] = relationship('JobApplication', back_populates='mobile_code')


class MasterModule(Base):
    __tablename__ = 'master_module'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_module_id'),
        UniqueConstraint('module_name', name='uk_master_module_module_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    master_sub_module: Mapped[list['MasterSubModule']] = relationship('MasterSubModule', back_populates='module')
    raw_material_details: Mapped[list['RawMaterialDetails']] = relationship('RawMaterialDetails', back_populates='module')
    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='module')
    user_services: Mapped[list['UserServices']] = relationship('UserServices', back_populates='module')
    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='module')


class MasterOwnershipType(Base):
    __tablename__ = 'master_ownership_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_ownership_type_id'),
        UniqueConstraint('ownership_type', name='uk_master_ownership_type_ownership_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ownership_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterParking(Base):
    __tablename__ = 'master_parking'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_parking_type_id'),
        UniqueConstraint('parking_type', name='uk_master_parking_type_parking_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parking_type: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterPaymentType(Base):
    __tablename__ = 'master_payment_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_payment_type_id'),
        UniqueConstraint('payment_name', name='uk_master_payment_type_payment_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='payment_type')


class MasterPharmacies(Base):
    __tablename__ = 'master_pharmacies'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_master_pharmacies_rating'),
        PrimaryKeyConstraint('id', name='pk_master_pharmacies_id'),
        UniqueConstraint('pharmacy_name', name='master_pharmacies_pharmacy_name_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    pharmacy_name: Mapped[str] = mapped_column(String(255), nullable=False)
    pharmacy_type: Mapped[Optional[str]] = mapped_column(String(100))
    services: Mapped[Optional[str]] = mapped_column(String(255))
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    delivery_time: Mapped[Optional[str]] = mapped_column(String(50))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))

    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='pharmacies')


class MasterPostedBy(Base):
    __tablename__ = 'master_posted_by'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_posted_by_id'),
        UniqueConstraint('posted_by', name='uk_master_posted_by_posted_by')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    posted_by: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterPreferredTenants(Base):
    __tablename__ = 'master_preferred_tenants'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_preferred_tenants_id'),
        UniqueConstraint('tenant_type', name='uk_master_preferred_tenants_tenant_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class MasterProductCategory(Base):
    __tablename__ = 'master_product_category'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_product_category_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    product_registration: Mapped[list['ProductRegistration']] = relationship('ProductRegistration', back_populates='category')


class MasterProject(Base):
    __tablename__ = 'master_project'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_project_id'),
        UniqueConstraint('project_name', name='uk_master_project')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    tasks: Mapped[list['Tasks']] = relationship('Tasks', back_populates='project')


class MasterPropertyType(Base):
    __tablename__ = 'master_property_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_property_type_id'),
        UniqueConstraint('property_type', name='uk_master_property_type_property_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='property_type')


class MasterRawMaterialType(Base):
    __tablename__ = 'master_raw_material_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_raw_material_type'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    raw_material_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    raw_material_details: Mapped[list['RawMaterialDetails']] = relationship('RawMaterialDetails', back_populates='raw_material_type')


class MasterRelation(Base):
    __tablename__ = 'master_relation'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_relation_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    relation_type: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    student_family_members: Mapped[list['StudentFamilyMembers']] = relationship('StudentFamilyMembers', back_populates='relation_type')


class MasterRole(Base):
    __tablename__ = 'master_role'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_role_id'),
        UniqueConstraint('role_name', name='uk_master_role_role_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[list['UserRegistration']] = relationship('UserRegistration', back_populates='role')
    user_role: Mapped[list['UserRole']] = relationship('UserRole', back_populates='role')
    freelancer_task_history: Mapped[list['FreelancerTaskHistory']] = relationship('FreelancerTaskHistory', back_populates='freelancer')


class MasterServiceType(Base):
    __tablename__ = 'master_service_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_service_type_id'),
        UniqueConstraint('service_type', name='uk_master_service_type_service_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_type: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='service_type')


class MasterSkill(Base):
    __tablename__ = 'master_skill'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_skill_id'),
        UniqueConstraint('skill', name='uk_master_skill_skill')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_skill: Mapped[list['JobSkill']] = relationship('JobSkill', back_populates='skill')
    user_skill: Mapped[list['UserSkill']] = relationship('UserSkill', back_populates='skill')


class MasterState(Base):
    __tablename__ = 'master_state'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_state_id'),
        UniqueConstraint('state_code', name='uk_master_state_state_code'),
        UniqueConstraint('state_name', name='uk_master_state_state_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    state_code: Mapped[int] = mapped_column(BigInteger, nullable=False)
    state_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    master_district: Mapped[list['MasterDistrict']] = relationship('MasterDistrict', back_populates='state')
    user_registration: Mapped[list['UserRegistration']] = relationship('UserRegistration', back_populates='state')


class MasterStatus(Base):
    __tablename__ = 'master_status'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_status_id'),
        UniqueConstraint('status_name', name='uk_master_status_status_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[list['UserRegistration']] = relationship('UserRegistration', back_populates='status')
    tasks: Mapped[list['Tasks']] = relationship('Tasks', back_populates='status')
    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='status')


class MasterStipendType(Base):
    __tablename__ = 'master_stipend_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_stipend_type_id'),
        UniqueConstraint('stipend_type', name='uk_master_stipend_type_stipend_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stipend_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_openings: Mapped[list['JobOpenings']] = relationship('JobOpenings', back_populates='stipend_type')


class MasterTaskType(Base):
    __tablename__ = 'master_task_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_task_type_id'),
        UniqueConstraint('task_type', name='uk_master_task_type_task_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_type: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    tasks: Mapped[list['Tasks']] = relationship('Tasks', back_populates='task_type')


class MasterTimeSlot(Base):
    __tablename__ = 'master_time_slot'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_time_slot_id'),
        UniqueConstraint('time_slot', name='uk_master_time_slot_time_slot')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time_slot: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='time_slot')
    vehicle_service_booking: Mapped[list['VehicleServiceBooking']] = relationship('VehicleServiceBooking', back_populates='time_slot')


class MasterVehicleBrand(Base):
    __tablename__ = 'master_vehicle_brand'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_vehicle_brand_id'),
        UniqueConstraint('brand_name', name='uk_master_vehicle_brand_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    vehicle_brand_fuel: Mapped[list['VehicleBrandFuel']] = relationship('VehicleBrandFuel', back_populates='brand')
    vehicle_service_booking: Mapped[list['VehicleServiceBooking']] = relationship('VehicleServiceBooking', back_populates='brand')


class MasterVehicleType(Base):
    __tablename__ = 'master_vehicle_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='master_vehicle_type_pkey'),
        UniqueConstraint('vehicle_type_name', name='master_vehicle_type_vehicle_type_name_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_type_name: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    product_order: Mapped[list['ProductOrder']] = relationship('ProductOrder', back_populates='vehicle_type')


class MasterWorkStatus(Base):
    __tablename__ = 'master_work_status'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_work_status_id'),
        UniqueConstraint('work_status_name', name='uk_master_work_status_work_status_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    work_status_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='work_status')
    freelancer_task_history: Mapped[list['FreelancerTaskHistory']] = relationship('FreelancerTaskHistory', back_populates='work_status')


class MasterWorkType(Base):
    __tablename__ = 'master_work_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_work_type_id'),
        UniqueConstraint('work_type', name='uk_master_work_type_work_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    work_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_openings: Mapped[list['JobOpenings']] = relationship('JobOpenings', back_populates='work_type')
    user_registration: Mapped[list['UserRegistration']] = relationship('UserRegistration', back_populates='work_type')


t_vw_active_job_openings = Table(
    'vw_active_job_openings', Base.metadata,
    Column('job_opening_id', BigInteger),
    Column('job_name', String(255)),
    Column('company_name', String(255)),
    Column('company_address', String(255)),
    Column('location_type_id', Integer),
    Column('location_type', String(255)),
    Column('work_type_id', Integer),
    Column('work_type', String(255)),
    Column('category_id', BigInteger),
    Column('category_name', String(100)),
    Column('internship_duration_id', BigInteger),
    Column('internship_duration', String(100)),
    Column('stipend_type_id', Integer),
    Column('stipend_type', String(50)),
    Column('role_description', String(500)),
    Column('requirements', String(500)),
    Column('created_date', DateTime)
)


t_vw_active_labs = Table(
    'vw_active_labs', Base.metadata,
    Column('lab_id', BigInteger),
    Column('lab_name', String(255)),
    Column('services', String(255)),
    Column('rating', Integer),
    Column('home_collection', Boolean),
    Column('latitude', Numeric(9, 6)),
    Column('longitude', Numeric(9, 6))
)


t_vw_available_doctors = Table(
    'vw_available_doctors', Base.metadata,
    Column('doctor_id', BigInteger),
    Column('doctor_name', Text),
    Column('specialization_id', BigInteger),
    Column('specialization_name', String(255)),
    Column('experience_years', Integer),
    Column('rating', Integer),
    Column('available_from', Time),
    Column('available_to', Time)
)


t_vw_company_list = Table(
    'vw_company_list', Base.metadata,
    Column('company_id', BigInteger),
    Column('company_name', String(255)),
    Column('location', String(255)),
    Column('industry_id', BigInteger),
    Column('industry_name', String(100)),
    Column('company_size_id', BigInteger),
    Column('company_size', String(50)),
    Column('jobs_count', BigInteger),
    Column('internships_count', BigInteger),
    Column('hiring_status', Text),
    Column('last_active_time', DateTime)
)


t_vw_nearby_ambulance_list = Table(
    'vw_nearby_ambulance_list', Base.metadata,
    Column('hospital_id', BigInteger),
    Column('hospital_name', String(255)),
    Column('specialty_type', String(50)),
    Column('location', String(255)),
    Column('latitude', Numeric(9, 6)),
    Column('longitude', Numeric(9, 6)),
    Column('hospital_contact', String(20)),
    Column('ambulance_id', BigInteger),
    Column('service_provider', String(100)),
    Column('ambulance_contact', String(20)),
    Column('availability_status', String(20))
)


t_vw_nearby_pharmacies = Table(
    'vw_nearby_pharmacies', Base.metadata,
    Column('pharmacy_id', BigInteger),
    Column('pharmacy_name', String(255)),
    Column('pharmacy_type', String(100)),
    Column('services', String(255)),
    Column('rating', Integer),
    Column('delivery_time', String(50)),
    Column('latitude', Numeric(9, 6)),
    Column('longitude', Numeric(9, 6))
)


t_vw_students_get_list = Table(
    'vw_students_get_list', Base.metadata,
    Column('user_id', BigInteger),
    Column('student_name', String),
    Column('joined_date', DateTime),
    Column('skill_id', Integer),
    Column('skill', String(255)),
    Column('attendance_percentage', Numeric(5, 2)),
    Column('aggregate', Text),
    Column('certificate_name', String(255)),
    Column('degree', String(255)),
    Column('internship_status', String(255)),
    Column('rating', Numeric)
)


class InstitutionRegistration(Base):
    __tablename__ = 'institution_registration'
    __table_args__ = (
        ForeignKeyConstraint(['identity_type_id'], ['master_identity_type.id'], name='fk_institution_registration_identity_type_id'),
        ForeignKeyConstraint(['institution_type_id'], ['master_institute_type.id'], name='fk_institution_registration_institution_type_id'),
        PrimaryKeyConstraint('id', name='pk_institution_registration_id'),
        UniqueConstraint('institution_name', 'identity_number', name='uk_institution_registration')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    institution_name: Mapped[str] = mapped_column(String(255), nullable=False)
    institution_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    identity_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    identity_number: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(500), nullable=False)
    representative_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(100), nullable=False)
    upload_id_proof: Mapped[Optional[str]] = mapped_column(String(500))
    upload_address_proof: Mapped[Optional[str]] = mapped_column(String(500))
    institute_website: Mapped[Optional[str]] = mapped_column(String(500))
    total_branches: Mapped[Optional[int]] = mapped_column(BigInteger)
    academic_year_start: Mapped[Optional[datetime.date]] = mapped_column(Date)
    academic_year_end: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    identity_type: Mapped['MasterIdentityType'] = relationship('MasterIdentityType', back_populates='institution_registration')
    institution_type: Mapped['MasterInstituteType'] = relationship('MasterInstituteType', back_populates='institution_registration')
    institution_branch: Mapped[list['InstitutionBranch']] = relationship('InstitutionBranch', back_populates='institution')
    otp_verification: Mapped[list['OtpVerification']] = relationship('OtpVerification', back_populates='institution')


class JobOpenings(Base):
    __tablename__ = 'job_openings'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['master_category.id'], name='fk_job_openings_category_id'),
        ForeignKeyConstraint(['company_size_id'], ['master_company_size.id'], name='fk_job_openings_company_size'),
        ForeignKeyConstraint(['industry_id'], ['master_industry.id'], name='fk_job_openings_industry'),
        ForeignKeyConstraint(['internship_duration_id'], ['master_internship_duration.id'], name='fk_job_openings_duration'),
        ForeignKeyConstraint(['job_id'], ['master_job.id'], name='fk_job_openings_job_id'),
        ForeignKeyConstraint(['location_type_id'], ['master_location_type.id'], name='fk_job_openings_location_type_id'),
        ForeignKeyConstraint(['stipend_type_id'], ['master_stipend_type.id'], name='fk_job_openings_stipend_type_id'),
        ForeignKeyConstraint(['work_type_id'], ['master_work_type.id'], name='fk_job_openings_work_type_id'),
        PrimaryKeyConstraint('id', name='pk_job_openings_id'),
        Index('idx_job_openings_job_id', 'job_id'),
        Index('idx_job_openings_location_type_id', 'location_type_id'),
        Index('idx_job_openings_work_type_id', 'work_type_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    job_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    company_address: Mapped[str] = mapped_column(String(255), nullable=False)
    location_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    work_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    role_description: Mapped[Optional[str]] = mapped_column(String(500))
    requirements: Mapped[Optional[str]] = mapped_column(String(500))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    sub_module_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    internship_stipend: Mapped[Optional[bool]] = mapped_column(Boolean)
    category_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    internship_duration_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    stipend_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    industry_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    company_size_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    category: Mapped[Optional['MasterCategory']] = relationship('MasterCategory', back_populates='job_openings')
    company_size: Mapped[Optional['MasterCompanySize']] = relationship('MasterCompanySize', back_populates='job_openings')
    industry: Mapped[Optional['MasterIndustry']] = relationship('MasterIndustry', back_populates='job_openings')
    internship_duration: Mapped[Optional['MasterInternshipDuration']] = relationship('MasterInternshipDuration', back_populates='job_openings')
    job: Mapped['MasterJob'] = relationship('MasterJob', back_populates='job_openings')
    location_type: Mapped['MasterLocationType'] = relationship('MasterLocationType', back_populates='job_openings')
    stipend_type: Mapped[Optional['MasterStipendType']] = relationship('MasterStipendType', back_populates='job_openings')
    work_type: Mapped['MasterWorkType'] = relationship('MasterWorkType', back_populates='job_openings')
    job_skill: Mapped[list['JobSkill']] = relationship('JobSkill', back_populates='job_openings')
    job_application: Mapped[list['JobApplication']] = relationship('JobApplication', back_populates='job_openings')


class MasterAmbulance(Base):
    __tablename__ = 'master_ambulance'
    __table_args__ = (
        ForeignKeyConstraint(['hospital_id'], ['master_hospital.id'], name='fk_ambulance_hospital'),
        PrimaryKeyConstraint('id', name='pk_master_ambulance_id'),
        UniqueConstraint('service_provider', name='uk_master_ambulance_service_provider')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    service_provider: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_number: Mapped[Optional[str]] = mapped_column(String(20))
    availability_status: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'Available'::character varying"))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    hospital_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    hospital: Mapped[Optional['MasterHospital']] = relationship('MasterHospital', back_populates='master_ambulance')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='ambulance')
    ambulance_booking: Mapped[list['AmbulanceBooking']] = relationship('AmbulanceBooking', back_populates='ambulance')


class MasterDesignation(Base):
    __tablename__ = 'master_designation'
    __table_args__ = (
        ForeignKeyConstraint(['dept_id'], ['master_department.id'], name='fk_master_designation_dept_id'),
        PrimaryKeyConstraint('id', name='pk_master_designation_id'),
        UniqueConstraint('designation_name', 'dept_id', name='uk_master_designation_designation_name_dept_id'),
        Index('idx_master_designation_dept_id', 'dept_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    designation_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    dept_id: Mapped[Optional[int]] = mapped_column(Integer)

    dept: Mapped[Optional['MasterDepartment']] = relationship('MasterDepartment', back_populates='master_designation')


class MasterDistrict(Base):
    __tablename__ = 'master_district'
    __table_args__ = (
        ForeignKeyConstraint(['state_id'], ['master_state.id'], name='fk_master_district_state_id'),
        PrimaryKeyConstraint('id', name='pk_master_district_id'),
        UniqueConstraint('district_code', name='uk_master_district_district_code'),
        UniqueConstraint('district_name', 'state_id', name='uk_master_district_district_name_state_id'),
        Index('idx_master_district_state_id', 'state_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    district_code: Mapped[int] = mapped_column(BigInteger, nullable=False)
    district_name: Mapped[str] = mapped_column(String(255), nullable=False)
    state_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    state: Mapped['MasterState'] = relationship('MasterState', back_populates='master_district')
    master_sub_district: Mapped[list['MasterSubDistrict']] = relationship('MasterSubDistrict', back_populates='district')
    user_registration: Mapped[list['UserRegistration']] = relationship('UserRegistration', back_populates='district')


class MasterSubModule(Base):
    __tablename__ = 'master_sub_module'
    __table_args__ = (
        ForeignKeyConstraint(['module_id'], ['master_module.id'], name='fk_master_sub_module_module_id'),
        PrimaryKeyConstraint('id', name='pk_master_sub_module_id'),
        UniqueConstraint('sub_module_name', 'module_id', name='uk_master_sub_module_sub_module_name_module_id'),
        Index('idx_master_sub_module_module_id', 'module_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_module_name: Mapped[str] = mapped_column(String(255), nullable=False)
    module_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    module: Mapped['MasterModule'] = relationship('MasterModule', back_populates='master_sub_module')
    master_service: Mapped[list['MasterService']] = relationship('MasterService', back_populates='sub_module')
    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='sub_module')
    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='sub_module')


class ProductRegistration(Base):
    __tablename__ = 'product_registration'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['master_product_category.id'], name='pk_product_registration_category_id'),
        PrimaryKeyConstraint('id', name='pk_product_registration_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    company_name: Mapped[Optional[str]] = mapped_column(String(255))
    product_name: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    product_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    product_image: Mapped[Optional[str]] = mapped_column(String(500))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))

    category: Mapped['MasterProductCategory'] = relationship('MasterProductCategory', back_populates='product_registration')
    product_order: Mapped[list['ProductOrder']] = relationship('ProductOrder', back_populates='product')
    product_rating: Mapped[list['ProductRating']] = relationship('ProductRating', back_populates='product')


class RawMaterialDetails(Base):
    __tablename__ = 'raw_material_details'
    __table_args__ = (
        ForeignKeyConstraint(['module_id'], ['master_module.id'], name='fk_raw_material_details_raw_module_id'),
        ForeignKeyConstraint(['raw_material_type_id'], ['master_raw_material_type.id'], name='fk_raw_material_details_raw_material_type_id'),
        PrimaryKeyConstraint('id', name='pk_raw_material_details_id'),
        Index('idx_raw_material_details_module_id', 'module_id'),
        Index('idx_raw_material_details_raw_material_type_id', 'raw_material_type_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    raw_material_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    latitude: Mapped[decimal.Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    longitude: Mapped[decimal.Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    module: Mapped['MasterModule'] = relationship('MasterModule', back_populates='raw_material_details')
    raw_material_type: Mapped['MasterRawMaterialType'] = relationship('MasterRawMaterialType', back_populates='raw_material_details')


class InstitutionBranch(Base):
    __tablename__ = 'institution_branch'
    __table_args__ = (
        ForeignKeyConstraint(['institution_id'], ['institution_registration.id'], name='fk_institution_branch_institution_institution_id'),
        PrimaryKeyConstraint('id', name='pk_institution_branch_id'),
        UniqueConstraint('branch_name', name='uq_institution_branch_branch_name'),
        UniqueConstraint('institution_id', 'branch_code', name='uk_institution_branch')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    institution_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    branch_name: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    branch_code: Mapped[str] = mapped_column(String(100), nullable=False)
    branch_head: Mapped[str] = mapped_column(String(255), nullable=False)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    student_count: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'ACTIVE'::character varying"))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)

    institution: Mapped['InstitutionRegistration'] = relationship('InstitutionRegistration', back_populates='institution_branch')
    exam_schedule: Mapped[list['ExamSchedule']] = relationship('ExamSchedule', back_populates='branch')
    student_profile: Mapped[list['StudentProfile']] = relationship('StudentProfile', foreign_keys='[StudentProfile.branch_id]', back_populates='branch')
    student_profile_: Mapped[list['StudentProfile']] = relationship('StudentProfile', foreign_keys='[StudentProfile.branch_name]', back_populates='institution_branch')


class JobSkill(Base):
    __tablename__ = 'job_skill'
    __table_args__ = (
        ForeignKeyConstraint(['job_openings_id'], ['job_openings.id'], name='fk_job_skill_job_openings_id'),
        ForeignKeyConstraint(['skill_id'], ['master_skill.id'], name='fk_job_skill_skill_id'),
        PrimaryKeyConstraint('id', name='pk_job_skill_id'),
        Index('idx_job_skill_job_openings_id', 'job_openings_id'),
        Index('idx_job_skill_skill_id', 'skill_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    job_openings_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    skill_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    job_openings: Mapped['JobOpenings'] = relationship('JobOpenings', back_populates='job_skill')
    skill: Mapped['MasterSkill'] = relationship('MasterSkill', back_populates='job_skill')


class MasterService(Base):
    __tablename__ = 'master_service'
    __table_args__ = (
        ForeignKeyConstraint(['sub_module_id'], ['master_sub_module.id'], name='fk_master_service_sub_module_id'),
        PrimaryKeyConstraint('id', name='pk_master_service_id'),
        UniqueConstraint('sub_module_id', 'service_name', name='uk_master_service_sub_module_id_service_name'),
        Index('idx_master_service_sub_module_id', 'sub_module_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_module_id: Mapped[int] = mapped_column(Integer, nullable=False)
    service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    sub_module: Mapped['MasterSubModule'] = relationship('MasterSubModule', back_populates='master_service')
    master_sub_service: Mapped[list['MasterSubService']] = relationship('MasterSubService', back_populates='service')
    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='service')
    property_sell_listing_service: Mapped[list['PropertySellListingService']] = relationship('PropertySellListingService', back_populates='service')


class MasterSubDistrict(Base):
    __tablename__ = 'master_sub_district'
    __table_args__ = (
        ForeignKeyConstraint(['district_id'], ['master_district.id'], name='fk_master_sub_district_district_id'),
        PrimaryKeyConstraint('id', name='pk_master_sub_district_id'),
        UniqueConstraint('sub_district_code', name='uk_master_sub_district_sub_district_code'),
        UniqueConstraint('sub_district_name', 'district_id', name='uk_master_sub_district_sub_district_name_district_id'),
        Index('idx_master_sub_district_district_id', 'district_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sub_district_code: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sub_district_name: Mapped[str] = mapped_column(String(255), nullable=False)
    district_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    district: Mapped['MasterDistrict'] = relationship('MasterDistrict', back_populates='master_sub_district')
    master_village: Mapped[list['MasterVillage']] = relationship('MasterVillage', back_populates='sub_district')


class OtpVerification(Base):
    __tablename__ = 'otp_verification'
    __table_args__ = (
        ForeignKeyConstraint(['institution_id'], ['institution_registration.id'], name='fk_otp_verification_institution_id'),
        PrimaryKeyConstraint('id', name='pk_otp_verification_id'),
        UniqueConstraint('identity_number', 'email', 'otp_code', name='uk_otp_verification')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    institution_id: Mapped[int] = mapped_column(Integer, nullable=False)
    identity_number: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    otp_code: Mapped[str] = mapped_column(String(10), nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    is_verified: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    institution: Mapped['InstitutionRegistration'] = relationship('InstitutionRegistration', back_populates='otp_verification')


class UserRegistration(Base):
    __tablename__ = 'user_registration'
    __table_args__ = (
        ForeignKeyConstraint(['business_type_id'], ['master_business_type.id'], name='fk_user_registration_business_type_id'),
        ForeignKeyConstraint(['district_id'], ['master_district.id'], name='fk_user_registration_district_id'),
        ForeignKeyConstraint(['gender_id'], ['master_gender.id'], name='fk_user_registration_gender_id'),
        ForeignKeyConstraint(['job_skill_id'], ['master_job_skill.id'], name='fk_user_registration_job_skill_id'),
        ForeignKeyConstraint(['role_id'], ['master_role.id'], name='fk_user_registration_role_id'),
        ForeignKeyConstraint(['state_id'], ['master_state.id'], name='fk_user_registration_state_id'),
        ForeignKeyConstraint(['status_id'], ['master_status.id'], name='fk_user_registration_status_id'),
        ForeignKeyConstraint(['work_type_id'], ['master_work_type.id'], name='fk_user_registration_work_type_id'),
        PrimaryKeyConstraint('id', name='pk_user_registration_id'),
        UniqueConstraint('email', name='uk_user_registration_email'),
        UniqueConstraint('mobile', name='uk_user_registration_mobile'),
        UniqueConstraint('unique_id', name='uk_user_registration_unique_id'),
        Index('idx_user_registration_business_type_id', 'business_type_id'),
        Index('idx_user_registration_district_id', 'district_id'),
        Index('idx_user_registration_gender_id', 'gender_id'),
        Index('idx_user_registration_job_skill_id', 'job_skill_id'),
        Index('idx_user_registration_role_id', 'role_id'),
        Index('idx_user_registration_state_id', 'state_id'),
        Index('idx_user_registration_status_id', 'status_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    mobile: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    unique_id: Mapped[str] = mapped_column(String(255), nullable=False)
    gender_id: Mapped[Optional[int]] = mapped_column(Integer)
    dob: Mapped[Optional[datetime.date]] = mapped_column(Date)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    role_id: Mapped[Optional[int]] = mapped_column(Integer)
    state_id: Mapped[Optional[int]] = mapped_column(Integer)
    district_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    profile_image: Mapped[Optional[str]] = mapped_column(String(500))
    experience_summary: Mapped[Optional[str]] = mapped_column(String)
    experience_doc: Mapped[Optional[str]] = mapped_column(String(500))
    government_id: Mapped[Optional[dict]] = mapped_column(JSON)
    address: Mapped[Optional[str]] = mapped_column(String)
    status_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    reg_payment_done: Mapped[Optional[bool]] = mapped_column(Boolean)
    reg_fee: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    experience_in_years: Mapped[Optional[str]] = mapped_column(String(255))
    noc_number: Mapped[Optional[str]] = mapped_column(String(255))
    police_station_name: Mapped[Optional[str]] = mapped_column(String(255))
    issue_year: Mapped[Optional[int]] = mapped_column(Integer)
    upload_noc: Mapped[Optional[str]] = mapped_column(String(500))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    business_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    product_name: Mapped[Optional[str]] = mapped_column(String(255))
    business_description: Mapped[Optional[str]] = mapped_column(String(255))
    org_name: Mapped[Optional[int]] = mapped_column(Integer)
    gst_number: Mapped[Optional[str]] = mapped_column(String(100))
    job_skill_id: Mapped[Optional[int]] = mapped_column(Integer)
    vehicle_insurance: Mapped[Optional[str]] = mapped_column(String(255))
    driver_license: Mapped[Optional[str]] = mapped_column(String(50))
    vehicle_rc: Mapped[Optional[str]] = mapped_column(String(50))
    pollution_certificate: Mapped[Optional[bool]] = mapped_column(Boolean)
    upload_pollution_certificate: Mapped[Optional[str]] = mapped_column(String(500))
    purchase_year: Mapped[Optional[datetime.date]] = mapped_column(Date)
    vehicle_model: Mapped[Optional[str]] = mapped_column(String(255))
    work_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    hospital_name: Mapped[Optional[str]] = mapped_column(String(255))
    upload_certificate: Mapped[Optional[str]] = mapped_column(String(500))
    doctor_designation: Mapped[Optional[str]] = mapped_column(String(255))

    business_type: Mapped[Optional['MasterBusinessType']] = relationship('MasterBusinessType', back_populates='user_registration')
    district: Mapped[Optional['MasterDistrict']] = relationship('MasterDistrict', back_populates='user_registration')
    gender: Mapped[Optional['MasterGender']] = relationship('MasterGender', back_populates='user_registration')
    job_skill: Mapped[Optional['MasterJobSkill']] = relationship('MasterJobSkill', back_populates='user_registration')
    role: Mapped[Optional['MasterRole']] = relationship('MasterRole', back_populates='user_registration')
    state: Mapped[Optional['MasterState']] = relationship('MasterState', back_populates='user_registration')
    status: Mapped[Optional['MasterStatus']] = relationship('MasterStatus', back_populates='user_registration')
    work_type: Mapped[Optional['MasterWorkType']] = relationship('MasterWorkType', back_populates='user_registration')
    doctor_profile: Mapped['DoctorProfile'] = relationship('DoctorProfile', uselist=False, back_populates='user')
    job_application: Mapped[list['JobApplication']] = relationship('JobApplication', back_populates='user')
    master_internship_status: Mapped[list['MasterInternshipStatus']] = relationship('MasterInternshipStatus', back_populates='user')
    product_order: Mapped[list['ProductOrder']] = relationship('ProductOrder', back_populates='user')
    product_rating: Mapped[list['ProductRating']] = relationship('ProductRating', back_populates='user')
    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', foreign_keys='[PropertySellListing.created_by]', back_populates='user_registration')
    property_sell_listing_: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', foreign_keys='[PropertySellListing.modified_by]', back_populates='user_registration_')
    property_sell_listing1: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', foreign_keys='[PropertySellListing.user_id]', back_populates='user')
    student_attendance: Mapped[list['StudentAttendance']] = relationship('StudentAttendance', back_populates='user')
    student_certificate: Mapped[list['StudentCertificate']] = relationship('StudentCertificate', foreign_keys='[StudentCertificate.created_by]', back_populates='user_registration')
    student_certificate_: Mapped[list['StudentCertificate']] = relationship('StudentCertificate', foreign_keys='[StudentCertificate.modified_by]', back_populates='user_registration_')
    student_certificate1: Mapped[list['StudentCertificate']] = relationship('StudentCertificate', foreign_keys='[StudentCertificate.user_id]', back_populates='user')
    student_family_members: Mapped[list['StudentFamilyMembers']] = relationship('StudentFamilyMembers', back_populates='user')
    student_qualification: Mapped[list['StudentQualification']] = relationship('StudentQualification', foreign_keys='[StudentQualification.created_by]', back_populates='user_registration')
    student_qualification_: Mapped[list['StudentQualification']] = relationship('StudentQualification', foreign_keys='[StudentQualification.modified_by]', back_populates='user_registration_')
    student_qualification1: Mapped[list['StudentQualification']] = relationship('StudentQualification', foreign_keys='[StudentQualification.user_id]', back_populates='user')
    tasks: Mapped[list['Tasks']] = relationship('Tasks', back_populates='user')
    user_role: Mapped[list['UserRole']] = relationship('UserRole', foreign_keys='[UserRole.created_by]', back_populates='user_registration')
    user_role_: Mapped[list['UserRole']] = relationship('UserRole', foreign_keys='[UserRole.modified_by]', back_populates='user_registration_')
    user_role1: Mapped[list['UserRole']] = relationship('UserRole', foreign_keys='[UserRole.user_id]', back_populates='user')
    user_services: Mapped[list['UserServices']] = relationship('UserServices', foreign_keys='[UserServices.created_by]', back_populates='user_registration')
    user_services_: Mapped[list['UserServices']] = relationship('UserServices', foreign_keys='[UserServices.modified_by]', back_populates='user_registration_')
    user_services1: Mapped[list['UserServices']] = relationship('UserServices', foreign_keys='[UserServices.user_id]', back_populates='user')
    user_skill: Mapped[list['UserSkill']] = relationship('UserSkill', foreign_keys='[UserSkill.created_by]', back_populates='user_registration')
    user_skill_: Mapped[list['UserSkill']] = relationship('UserSkill', foreign_keys='[UserSkill.modified_by]', back_populates='user_registration_')
    user_skill1: Mapped[list['UserSkill']] = relationship('UserSkill', foreign_keys='[UserSkill.user_id]', back_populates='user')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='user')
    home_service: Mapped[list['HomeService']] = relationship('HomeService', foreign_keys='[HomeService.assigned_to]', back_populates='user_registration')
    home_service_: Mapped[list['HomeService']] = relationship('HomeService', foreign_keys='[HomeService.created_by]', back_populates='user_registration_')
    home_service1: Mapped[list['HomeService']] = relationship('HomeService', foreign_keys='[HomeService.modified_by]', back_populates='user_registration1')
    property_listing: Mapped[list['PropertyListing']] = relationship('PropertyListing', foreign_keys='[PropertyListing.created_by]', back_populates='user_registration')
    property_listing_: Mapped[list['PropertyListing']] = relationship('PropertyListing', foreign_keys='[PropertyListing.modified_by]', back_populates='user_registration_')
    property_listing1: Mapped[list['PropertyListing']] = relationship('PropertyListing', foreign_keys='[PropertyListing.user_id]', back_populates='user')
    task_history: Mapped[list['TaskHistory']] = relationship('TaskHistory', foreign_keys='[TaskHistory.from_assignee_id]', back_populates='from_assignee')
    task_history_: Mapped[list['TaskHistory']] = relationship('TaskHistory', foreign_keys='[TaskHistory.reporting_manager_id]', back_populates='reporting_manager')
    task_history1: Mapped[list['TaskHistory']] = relationship('TaskHistory', foreign_keys='[TaskHistory.to_assignee_id]', back_populates='to_assignee')
    task_history2: Mapped[list['TaskHistory']] = relationship('TaskHistory', foreign_keys='[TaskHistory.user_id]', back_populates='user')
    freelancer_task_history: Mapped[list['FreelancerTaskHistory']] = relationship('FreelancerTaskHistory', foreign_keys='[FreelancerTaskHistory.created_by]', back_populates='user_registration')
    freelancer_task_history_: Mapped[list['FreelancerTaskHistory']] = relationship('FreelancerTaskHistory', foreign_keys='[FreelancerTaskHistory.modified_by]', back_populates='user_registration_')
    hs_add_on: Mapped[list['HsAddOn']] = relationship('HsAddOn', foreign_keys='[HsAddOn.created_by]', back_populates='user_registration')
    hs_add_on_: Mapped[list['HsAddOn']] = relationship('HsAddOn', foreign_keys='[HsAddOn.modified_by]', back_populates='user_registration_')
    vehicle_service_booking: Mapped[list['VehicleServiceBooking']] = relationship('VehicleServiceBooking', foreign_keys='[VehicleServiceBooking.created_by]', back_populates='user_registration')
    vehicle_service_booking_: Mapped[list['VehicleServiceBooking']] = relationship('VehicleServiceBooking', foreign_keys='[VehicleServiceBooking.modified_by]', back_populates='user_registration_')
    vehicle_service_booking1: Mapped[list['VehicleServiceBooking']] = relationship('VehicleServiceBooking', foreign_keys='[VehicleServiceBooking.user_id]', back_populates='user')


class DoctorProfile(Base):
    __tablename__ = 'doctor_profile'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_doctor_profile_rating'),
        ForeignKeyConstraint(['specialization_id'], ['master_doctor_specialization.id'], name='fk_doctor_profile_specialization_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_doctor_profile_user_id'),
        PrimaryKeyConstraint('id', name='pk_doctor_profile_id'),
        UniqueConstraint('user_id', name='uk_doctor_profile_user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    specialization_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    experience_years: Mapped[Optional[int]] = mapped_column(Integer)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    fees_per_hour: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    available_from: Mapped[Optional[datetime.time]] = mapped_column(Time)
    available_to: Mapped[Optional[datetime.time]] = mapped_column(Time)
    is_available: Mapped[Optional[bool]] = mapped_column(Boolean)

    specialization: Mapped['MasterDoctorSpecialization'] = relationship('MasterDoctorSpecialization', back_populates='doctor_profile')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='doctor_profile')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='doctor')


class ExamSchedule(Base):
    __tablename__ = 'exam_schedule'
    __table_args__ = (
        ForeignKeyConstraint(['branch_id'], ['institution_branch.id'], name='fk_exam_schedule_branch_branch_id'),
        PrimaryKeyConstraint('id', name='pk_exam_schedule_id'),
        UniqueConstraint('branch_id', 'exam_type', 'subject_name', 'exam_date', name='uk_exam_schedule')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    exam_type: Mapped[str] = mapped_column(String(100), nullable=False)
    subject_name: Mapped[str] = mapped_column(String(100), nullable=False)
    exam_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    branch: Mapped['InstitutionBranch'] = relationship('InstitutionBranch', back_populates='exam_schedule')


class JobApplication(Base):
    __tablename__ = 'job_application'
    __table_args__ = (
        CheckConstraint('fresher = true AND experienced = false AND company IS NULL AND from_date IS NULL AND to_date IS NULL AND company_city_id IS NULL AND current_ctc IS NULL OR fresher = false AND experienced = true AND company IS NOT NULL AND from_date IS NOT NULL AND to_date IS NOT NULL AND company_city_id IS NOT NULL AND current_ctc IS NOT NULL', name='ck_job_application_fresher_experienced'),
        ForeignKeyConstraint(['city_id'], ['master_city.id'], name='fk_job_application_city_id'),
        ForeignKeyConstraint(['company_city_id'], ['master_city.id'], name='fk_job_application_company_city_id'),
        ForeignKeyConstraint(['job_openings_id'], ['job_openings.id'], name='fk_job_application_job_openings_id'),
        ForeignKeyConstraint(['mobile_code_id'], ['master_mobile_code.id'], name='fk_job_application_mobile_code_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_job_application_user_id'),
        PrimaryKeyConstraint('id', name='pk_job_application_id'),
        Index('idx_job_application_city_id', 'city_id'),
        Index('idx_job_application_company_city_id', 'company_city_id'),
        Index('idx_job_application_job_openings_id', 'job_openings_id'),
        Index('idx_job_application_mobile_code_id', 'mobile_code_id'),
        Index('idx_job_application_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    job_openings_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    mobile_number: Mapped[str] = mapped_column(String(255), nullable=False)
    mobile_code_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    city_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    upload_resume: Mapped[str] = mapped_column(String(500), nullable=False)
    notice_period_in_days: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    company: Mapped[Optional[str]] = mapped_column(String(255))
    from_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    to_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    company_city_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    current_ctc: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    expected_ctc: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    fresher: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    experienced: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    city: Mapped['MasterCity'] = relationship('MasterCity', foreign_keys=[city_id], back_populates='job_application')
    company_city: Mapped[Optional['MasterCity']] = relationship('MasterCity', foreign_keys=[company_city_id], back_populates='job_application_')
    job_openings: Mapped['JobOpenings'] = relationship('JobOpenings', back_populates='job_application')
    mobile_code: Mapped['MasterMobileCode'] = relationship('MasterMobileCode', back_populates='job_application')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='job_application')


class MasterInternshipStatus(Base):
    __tablename__ = 'master_internship_status'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_master_internship_status_user_id'),
        PrimaryKeyConstraint('id', name='pk_master_internship_status_id'),
        Index('idx_master_internship_status_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    internship_status: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    user: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', back_populates='master_internship_status')


class MasterSubService(Base):
    __tablename__ = 'master_sub_service'
    __table_args__ = (
        ForeignKeyConstraint(['service_id'], ['master_service.id'], name='fk_master_sub_service_service_id'),
        PrimaryKeyConstraint('id', name='pk_master_sub_service_id'),
        UniqueConstraint('sub_service_name', 'service_id', name='uk_master_sub_service_sub_service_name_service_id'),
        Index('idx_master_sub_service_service_id', 'service_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    service_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    service: Mapped['MasterService'] = relationship('MasterService', back_populates='master_sub_service')
    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='sub_service')
    master_garage: Mapped[list['MasterGarage']] = relationship('MasterGarage', back_populates='sub_service')
    master_garage_service: Mapped[list['MasterGarageService']] = relationship('MasterGarageService', back_populates='sub_service')
    master_sub_group: Mapped[list['MasterSubGroup']] = relationship('MasterSubGroup', back_populates='sub_service')
    vehicle_brand_fuel: Mapped[list['VehicleBrandFuel']] = relationship('VehicleBrandFuel', back_populates='sub_service')
    vehicle_service_booking: Mapped[list['VehicleServiceBooking']] = relationship('VehicleServiceBooking', back_populates='sub_service')


class MasterVillage(Base):
    __tablename__ = 'master_village'
    __table_args__ = (
        ForeignKeyConstraint(['sub_district_id'], ['master_sub_district.id'], name='fk_master_village_sub_district_id'),
        PrimaryKeyConstraint('id', name='pk_master_village_id'),
        UniqueConstraint('village_code', name='uk_master_village_village_code'),
        Index('idx_master_village_sub_district_id', 'sub_district_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    village_code: Mapped[int] = mapped_column(BigInteger, nullable=False)
    village_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sub_district_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    sub_district: Mapped['MasterSubDistrict'] = relationship('MasterSubDistrict', back_populates='master_village')


class ProductOrder(Base):
    __tablename__ = 'product_order'
    __table_args__ = (
        ForeignKeyConstraint(['product_id'], ['product_registration.id'], name='fk_product_order_product_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_product_order_user_id'),
        ForeignKeyConstraint(['vehicle_type_id'], ['master_vehicle_type.id'], name='fk_product_order_vehicle_type_id'),
        PrimaryKeyConstraint('id', name='pk_product_order_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    delivery_address: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[str] = mapped_column(String(50), nullable=False)
    vehicle_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    order_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'Pending'::character varying"))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    product: Mapped['ProductRegistration'] = relationship('ProductRegistration', back_populates='product_order')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='product_order')
    vehicle_type: Mapped[Optional['MasterVehicleType']] = relationship('MasterVehicleType', back_populates='product_order')


class ProductRating(Base):
    __tablename__ = 'product_rating'
    __table_args__ = (
        ForeignKeyConstraint(['product_id'], ['product_registration.id'], name='fk_product_rating_product_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_product_rating_user_id'),
        PrimaryKeyConstraint('id', name='pk_product_rating_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    rating: Mapped[decimal.Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    product: Mapped['ProductRegistration'] = relationship('ProductRegistration', back_populates='product_rating')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='product_rating')


class PropertySellListing(Base):
    __tablename__ = 'property_sell_listing'
    __table_args__ = (
        ForeignKeyConstraint(['bhk_type_id'], ['master_bhk_type.id'], name='fk_property_sell_listing_bhk_type_id'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_property_sell_listing_created_by'),
        ForeignKeyConstraint(['furnishing_id'], ['master_furnishing.id'], name='fk_property_sell_listing_furnishing_id'),
        ForeignKeyConstraint(['hostel_type_id'], ['master_hostel_type.id'], name='fk_property_sell_listing_hostel_type_id'),
        ForeignKeyConstraint(['item_condition_id'], ['master_item_condition.id'], name='fk_property_sell_listing_item_condition_id'),
        ForeignKeyConstraint(['listing_type_id'], ['master_listing_type.id'], name='fk_property_sell_listing_listing_type_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_property_sell_listing_modified_by'),
        ForeignKeyConstraint(['module_id'], ['master_module.id'], name='fk_property_sell_listing_module_id'),
        ForeignKeyConstraint(['property_type_id'], ['master_property_type.id'], name='fk_property_sell_listing_property_type_id'),
        ForeignKeyConstraint(['sub_module_id'], ['master_sub_module.id'], name='fk_property_sell_listing_sub_module_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_property_sell_listing_user_id'),
        PrimaryKeyConstraint('id', name='pk_property_sell_listing'),
        Index('idx_property_sell_listing_bhk_type_id', 'bhk_type_id'),
        Index('idx_property_sell_listing_created_by', 'created_by'),
        Index('idx_property_sell_listing_furnishing_id', 'furnishing_id'),
        Index('idx_property_sell_listing_modified_by', 'modified_by'),
        Index('idx_property_sell_listing_module_id', 'module_id'),
        Index('idx_property_sell_listing_property_type_id', 'property_type_id'),
        Index('idx_property_sell_listing_sub_module_id', 'sub_module_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sub_module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    bhk_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    furnishing_id: Mapped[int] = mapped_column(Integer, nullable=False)
    locality_area: Mapped[str] = mapped_column(String(255), nullable=False)
    upload_photos: Mapped[str] = mapped_column(String(500), nullable=False)
    property_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    expected_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    monthly_rent: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    property_description: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    item_condition_id: Mapped[Optional[int]] = mapped_column(Integer)
    hostel_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    total_rooms: Mapped[Optional[int]] = mapped_column(Integer)
    available_rooms: Mapped[Optional[int]] = mapped_column(Integer)
    food_included: Mapped[Optional[bool]] = mapped_column(Boolean)
    location: Mapped[Optional[int]] = mapped_column(Integer)
    rating: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    listing_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    property_sqft: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    bhk_type: Mapped['MasterBhkType'] = relationship('MasterBhkType', back_populates='property_sell_listing')
    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='property_sell_listing')
    furnishing: Mapped['MasterFurnishing'] = relationship('MasterFurnishing', back_populates='property_sell_listing')
    hostel_type: Mapped[Optional['MasterHostelType']] = relationship('MasterHostelType', back_populates='property_sell_listing')
    item_condition: Mapped[Optional['MasterItemCondition']] = relationship('MasterItemCondition', back_populates='property_sell_listing')
    listing_type: Mapped[Optional['MasterListingType']] = relationship('MasterListingType', back_populates='property_sell_listing')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='property_sell_listing_')
    module: Mapped['MasterModule'] = relationship('MasterModule', back_populates='property_sell_listing')
    property_type: Mapped[Optional['MasterPropertyType']] = relationship('MasterPropertyType', back_populates='property_sell_listing')
    sub_module: Mapped['MasterSubModule'] = relationship('MasterSubModule', back_populates='property_sell_listing')
    user: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='property_sell_listing1')
    property_listing: Mapped[list['PropertyListing']] = relationship('PropertyListing', back_populates='property_sell_listing')
    property_sell_listing_service: Mapped[list['PropertySellListingService']] = relationship('PropertySellListingService', back_populates='property_sell_listing')


class StudentAttendance(Base):
    __tablename__ = 'student_attendance'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_student_attendance_user_id'),
        PrimaryKeyConstraint('id', name='pk_student_attendance_id'),
        Index('idx_student_attendance_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    attendance_percentage: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', back_populates='student_attendance')


class StudentCertificate(Base):
    __tablename__ = 'student_certificate'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_student_certificate_created_by'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_student_certificate_modified_by'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_student_certificate_user_id'),
        PrimaryKeyConstraint('id', name='pk_student_certificate_id'),
        Index('idx_student_certificate_created_by', 'created_by'),
        Index('idx_student_certificate_modified_by', 'modified_by'),
        Index('idx_student_certificate_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    certificate_name: Mapped[str] = mapped_column(String(255), nullable=False)
    issued_by: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    upload_certificate: Mapped[str] = mapped_column(String(500), nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='student_certificate')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='student_certificate_')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='student_certificate1')


class StudentFamilyMembers(Base):
    __tablename__ = 'student_family_members'
    __table_args__ = (
        ForeignKeyConstraint(['relation_type_id'], ['master_relation.id'], name='fk_student_family_members_relation_type_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_student_family_members_user_id'),
        PrimaryKeyConstraint('id', name='pk_student_family_members_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    relation_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    phone_number: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    relation_type: Mapped['MasterRelation'] = relationship('MasterRelation', back_populates='student_family_members')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='student_family_members')


class StudentProfile(Base):
    __tablename__ = 'student_profile'
    __table_args__ = (
        ForeignKeyConstraint(['branch_id'], ['institution_branch.id'], name='fk_student_profile_branch_id'),
        ForeignKeyConstraint(['branch_name'], ['institution_branch.branch_name'], name='fk_student_profile_branch_name'),
        PrimaryKeyConstraint('id', name='pk_student_profile_id'),
        UniqueConstraint('student_id', name='uk_student_profile_student_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    branch_name: Mapped[str] = mapped_column(String(255), nullable=False)
    student_name: Mapped[str] = mapped_column(String(255), nullable=False)
    student_id: Mapped[str] = mapped_column(String(150), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(100), nullable=False)
    profile_image_url: Mapped[Optional[str]] = mapped_column(String(500))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    parent_mobile: Mapped[Optional[str]] = mapped_column(String(100))

    branch: Mapped['InstitutionBranch'] = relationship('InstitutionBranch', foreign_keys=[branch_id], back_populates='student_profile')
    institution_branch: Mapped['InstitutionBranch'] = relationship('InstitutionBranch', foreign_keys=[branch_name], back_populates='student_profile_')
    student_academic_finance: Mapped['StudentAcademicFinance'] = relationship('StudentAcademicFinance', uselist=False, back_populates='student')
    student_fee_installments: Mapped[list['StudentFeeInstallments']] = relationship('StudentFeeInstallments', back_populates='student')


class StudentQualification(Base):
    __tablename__ = 'student_qualification'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_student_qualification_created_by'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_student_qualification_modified_by'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_student_qualification_user_id'),
        PrimaryKeyConstraint('id', name='pk_student_qualification_id'),
        Index('idx_student_qualification_created_by', 'created_by'),
        Index('idx_student_qualification_modified_by', 'modified_by'),
        Index('idx_student_qualification_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    degree: Mapped[str] = mapped_column(String(255), nullable=False)
    institute: Mapped[str] = mapped_column(String(255), nullable=False)
    percentage: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='student_qualification')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='student_qualification_')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='student_qualification1')


class Tasks(Base):
    __tablename__ = 'tasks'
    __table_args__ = (
        ForeignKeyConstraint(['project_id'], ['master_project.id'], name='fk_tasks_project_id'),
        ForeignKeyConstraint(['status_id'], ['master_status.id'], name='fk_tasks_status_id'),
        ForeignKeyConstraint(['task_type_id'], ['master_task_type.id'], name='fk_tasks_task_type_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_tasks_user_id'),
        PrimaryKeyConstraint('id', name='pk_tasks_id'),
        UniqueConstraint('title', 'task_type_id', 'project_id', 'user_id', 'status_id', name='uk_tasks_title_task_type_id_project_id_user_id_status_id'),
        Index('idx_tasks_project_id', 'project_id'),
        Index('idx_tasks_status_id', 'status_id'),
        Index('idx_tasks_task_type_id', 'task_type_id'),
        Index('idx_tasks_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    task_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    reporting_manager_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    task_manager_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    efforts_in_days: Mapped[Optional[int]] = mapped_column(Integer)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    project: Mapped['MasterProject'] = relationship('MasterProject', back_populates='tasks')
    status: Mapped['MasterStatus'] = relationship('MasterStatus', back_populates='tasks')
    task_type: Mapped['MasterTaskType'] = relationship('MasterTaskType', back_populates='tasks')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='tasks')
    task_history: Mapped[list['TaskHistory']] = relationship('TaskHistory', back_populates='task')


class UserRole(Base):
    __tablename__ = 'user_role'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_user_role_created_by'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_user_role_modified_by'),
        ForeignKeyConstraint(['role_id'], ['master_role.id'], name='fk_user_role_role_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_user_role_user_id'),
        PrimaryKeyConstraint('id', name='pk_user_role_id'),
        UniqueConstraint('user_id', 'role_id', name='uk_user_role_user_id_role_id'),
        Index('idx_user_role_created_by', 'created_by'),
        Index('idx_user_role_modified_by', 'modified_by'),
        Index('idx_user_role_role_id', 'role_id'),
        Index('idx_user_role_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    role_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='user_role')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='user_role_')
    role: Mapped['MasterRole'] = relationship('MasterRole', back_populates='user_role')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='user_role1')


class UserServices(Base):
    __tablename__ = 'user_services'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_user_services_created_by'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_user_services_modified_by'),
        ForeignKeyConstraint(['module_id'], ['master_module.id'], name='fk_user_services_module_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_user_services_user_id'),
        PrimaryKeyConstraint('id', name='pk_user_services_id'),
        Index('idx_user_services_created_by', 'created_by'),
        Index('idx_user_services_modified_by', 'modified_by'),
        Index('idx_user_services_module_id', 'module_id'),
        Index('idx_user_services_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='user_services')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='user_services_')
    module: Mapped['MasterModule'] = relationship('MasterModule', back_populates='user_services')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='user_services1')


class UserSkill(Base):
    __tablename__ = 'user_skill'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_user_skill_created_by'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_user_skill_modified_by'),
        ForeignKeyConstraint(['skill_id'], ['master_skill.id'], name='fk_user_skill_skill_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_user_skill_user_id'),
        PrimaryKeyConstraint('id', name='pk_user_skill_id'),
        Index('idx_user_skill_created_by', 'created_by'),
        Index('idx_user_skill_modified_by', 'modified_by'),
        Index('idx_user_skill_skill_id', 'skill_id'),
        Index('idx_user_skill_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='user_skill')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='user_skill_')
    skill: Mapped['MasterSkill'] = relationship('MasterSkill', back_populates='user_skill')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='user_skill1')


class Appointments(Base):
    __tablename__ = 'appointments'
    __table_args__ = (
        ForeignKeyConstraint(['ambulance_id'], ['master_ambulance.id'], name='fk_appointments_ambulance_id'),
        ForeignKeyConstraint(['assistant_id'], ['master_assistants.id'], name='fk_appointments_assistant_id'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profile.id'], name='fk_appointments_doctor_id'),
        ForeignKeyConstraint(['doctor_specialization_id'], ['master_doctor_specialization.id'], name='fk_appointments_doctor_specialization_id'),
        ForeignKeyConstraint(['labs_id'], ['master_labs.id'], name='fk_appointments_labs_id'),
        ForeignKeyConstraint(['pharmacies_id'], ['master_pharmacies.id'], name='fk_appointments_pharmacies_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_appointments_user_id'),
        PrimaryKeyConstraint('id', name='pk_appointments_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    consultation_type: Mapped[str] = mapped_column(String(20), nullable=False)
    appointment_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    doctor_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    doctor_specialization_id: Mapped[Optional[int]] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(String)
    days_of_suffering: Mapped[Optional[int]] = mapped_column(Integer)
    health_insurance: Mapped[Optional[bool]] = mapped_column(Boolean)
    upload_prescription: Mapped[Optional[str]] = mapped_column(String(500))
    upload_test_list: Mapped[Optional[str]] = mapped_column(String(500))
    required_ambulance: Mapped[Optional[bool]] = mapped_column(Boolean)
    required_assistant: Mapped[Optional[bool]] = mapped_column(Boolean)
    ambulance_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    pickup_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    assistant_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    pharmacies_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    labs_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    ambulance: Mapped[Optional['MasterAmbulance']] = relationship('MasterAmbulance', back_populates='appointments')
    assistant: Mapped[Optional['MasterAssistants']] = relationship('MasterAssistants', back_populates='appointments')
    doctor: Mapped[Optional['DoctorProfile']] = relationship('DoctorProfile', back_populates='appointments')
    doctor_specialization: Mapped[Optional['MasterDoctorSpecialization']] = relationship('MasterDoctorSpecialization', back_populates='appointments')
    labs: Mapped[Optional['MasterLabs']] = relationship('MasterLabs', back_populates='appointments')
    pharmacies: Mapped[Optional['MasterPharmacies']] = relationship('MasterPharmacies', back_populates='appointments')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='appointments')
    ambulance_booking: Mapped[list['AmbulanceBooking']] = relationship('AmbulanceBooking', back_populates='appointment')


class HomeService(Base):
    __tablename__ = 'home_service'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_home_service_rating'),
        ForeignKeyConstraint(['assigned_to'], ['user_registration.id'], name='fk_home_service_assigned_to'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_home_service_created_by'),
        ForeignKeyConstraint(['duration_id'], ['master_duration.id'], name='fk_home_service_duration_id'),
        ForeignKeyConstraint(['issue_id'], ['master_issue.id'], name='fk_home_service_issue_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_home_service_modified_by'),
        ForeignKeyConstraint(['module_id'], ['master_module.id'], name='fk_home_service_module_id'),
        ForeignKeyConstraint(['payment_type_id'], ['master_payment_type.id'], name='fk_home_service_payment_type_id'),
        ForeignKeyConstraint(['service_id'], ['master_service.id'], name='fk_home_service_service_id'),
        ForeignKeyConstraint(['service_type_id'], ['master_service_type.id'], name='fk_home_service_service_type_id'),
        ForeignKeyConstraint(['status_id'], ['master_status.id'], name='fk_home_service_status_id'),
        ForeignKeyConstraint(['sub_module_id'], ['master_sub_module.id'], name='fk_home_service_sub_module_id'),
        ForeignKeyConstraint(['sub_service_id'], ['master_sub_service.id'], name='fk_home_service_sub_service_id'),
        ForeignKeyConstraint(['time_slot_id'], ['master_time_slot.id'], name='fk_home_service_time_slot_id'),
        ForeignKeyConstraint(['work_status_id'], ['master_work_status.id'], name='fk_home_service_work_status_id'),
        PrimaryKeyConstraint('id', name='pk_home_service_id'),
        Index('idx_home_service_assigned_to', 'assigned_to'),
        Index('idx_home_service_created_by', 'created_by'),
        Index('idx_home_service_duration_id', 'duration_id'),
        Index('idx_home_service_issue_id', 'issue_id'),
        Index('idx_home_service_modified_by', 'modified_by'),
        Index('idx_home_service_module_id', 'module_id'),
        Index('idx_home_service_payment_type_id', 'payment_type_id'),
        Index('idx_home_service_service_id', 'service_id'),
        Index('idx_home_service_service_type_id', 'service_type_id'),
        Index('idx_home_service_status_id', 'status_id'),
        Index('idx_home_service_sub_module_id', 'sub_module_id'),
        Index('idx_home_service_sub_service_id', 'sub_service_id'),
        Index('idx_home_service_time_slot_id', 'time_slot_id'),
        Index('idx_home_service_work_status_id', 'work_status_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sub_module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    service_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    mobile: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    sub_service_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    service_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    issue_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    problem_description: Mapped[Optional[str]] = mapped_column(String(500))
    property_size_sqft: Mapped[Optional[str]] = mapped_column(String(150))
    preferred_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    time_slot_id: Mapped[Optional[int]] = mapped_column(Integer)
    special_instructions: Mapped[Optional[str]] = mapped_column(String(500))
    payment_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    service_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    payment_done: Mapped[Optional[bool]] = mapped_column(Boolean)
    assigned_to: Mapped[Optional[int]] = mapped_column(BigInteger)
    status_id: Mapped[Optional[int]] = mapped_column(Integer)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    duration_id: Mapped[Optional[int]] = mapped_column(Integer)
    others_address: Mapped[Optional[str]] = mapped_column(String(255))
    work_status_id: Mapped[Optional[int]] = mapped_column(Integer)
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[assigned_to], back_populates='home_service')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='home_service_')
    duration: Mapped[Optional['MasterDuration']] = relationship('MasterDuration', back_populates='home_service')
    issue: Mapped[Optional['MasterIssue']] = relationship('MasterIssue', back_populates='home_service')
    user_registration1: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='home_service1')
    module: Mapped['MasterModule'] = relationship('MasterModule', back_populates='home_service')
    payment_type: Mapped[Optional['MasterPaymentType']] = relationship('MasterPaymentType', back_populates='home_service')
    service: Mapped['MasterService'] = relationship('MasterService', back_populates='home_service')
    service_type: Mapped[Optional['MasterServiceType']] = relationship('MasterServiceType', back_populates='home_service')
    status: Mapped[Optional['MasterStatus']] = relationship('MasterStatus', back_populates='home_service')
    sub_module: Mapped['MasterSubModule'] = relationship('MasterSubModule', back_populates='home_service')
    sub_service: Mapped[Optional['MasterSubService']] = relationship('MasterSubService', back_populates='home_service')
    time_slot: Mapped[Optional['MasterTimeSlot']] = relationship('MasterTimeSlot', back_populates='home_service')
    work_status: Mapped[Optional['MasterWorkStatus']] = relationship('MasterWorkStatus', back_populates='home_service')
    freelancer_task_history: Mapped[list['FreelancerTaskHistory']] = relationship('FreelancerTaskHistory', back_populates='home_service')
    hs_add_on: Mapped[list['HsAddOn']] = relationship('HsAddOn', back_populates='home_service')


class MasterGarage(Base):
    __tablename__ = 'master_garage'
    __table_args__ = (
        ForeignKeyConstraint(['sub_service_id'], ['master_sub_service.id'], name='fk_master_garage_sub_service_id'),
        PrimaryKeyConstraint('id', name='pk_master_garage_id'),
        UniqueConstraint('garage_name', 'sub_service_id', name='uk_master_garage_name_sub_service')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    garage_name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    sub_service_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    rating: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(2, 1))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    sub_service: Mapped['MasterSubService'] = relationship('MasterSubService', back_populates='master_garage')
    master_mechanic: Mapped[list['MasterMechanic']] = relationship('MasterMechanic', back_populates='garage')
    vehicle_service_booking: Mapped[list['VehicleServiceBooking']] = relationship('VehicleServiceBooking', back_populates='garage')


class MasterGarageService(Base):
    __tablename__ = 'master_garage_service'
    __table_args__ = (
        ForeignKeyConstraint(['sub_service_id'], ['master_sub_service.id'], name='fk_master_garage_service_sub_service_id'),
        PrimaryKeyConstraint('id', name='pk_master_garage_service_id'),
        UniqueConstraint('sub_service_id', 'service_name', name='uk_master_garage_service')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_service_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    sub_service: Mapped['MasterSubService'] = relationship('MasterSubService', back_populates='master_garage_service')
    booking_service_mapping: Mapped[list['BookingServiceMapping']] = relationship('BookingServiceMapping', back_populates='garage_service')


class MasterSubGroup(Base):
    __tablename__ = 'master_sub_group'
    __table_args__ = (
        ForeignKeyConstraint(['sub_service_id'], ['master_sub_service.id'], name='fk_master_sub_group_sub_service_id'),
        PrimaryKeyConstraint('id', name='pk_master_sub_group_id'),
        UniqueConstraint('sub_service_id', 'sub_group_name', name='uk_master_sub_group_sub_service_id_sub_group_name'),
        Index('idx_master_sub_group_sub_service_id', 'sub_service_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sub_service_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_group_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    sub_service: Mapped['MasterSubService'] = relationship('MasterSubService', back_populates='master_sub_group')


class PropertyListing(Base):
    __tablename__ = 'property_listing'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_property_listing_rating'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_property_listing_created_by'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_property_listing_modified_by'),
        ForeignKeyConstraint(['property_sell_listing_id'], ['property_sell_listing.id'], name='fk_property_listing_property_sell_listing_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_property_listing_user_id'),
        PrimaryKeyConstraint('id', name='pk_property_listing_id'),
        Index('idx_property_listing_created_by', 'created_by'),
        Index('idx_property_listing_modified_by', 'modified_by'),
        Index('idx_property_listing_property_sell_listing_id', 'property_sell_listing_id'),
        Index('idx_property_listing_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    property_sell_listing_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    mobile_number: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    rating: Mapped[Optional[int]] = mapped_column(Integer)

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='property_listing')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='property_listing_')
    property_sell_listing: Mapped['PropertySellListing'] = relationship('PropertySellListing', back_populates='property_listing')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='property_listing1')


class PropertySellListingService(Base):
    __tablename__ = 'property_sell_listing_service'
    __table_args__ = (
        ForeignKeyConstraint(['property_sell_listing_id'], ['property_sell_listing.id'], name='fk_property_sell_listing_service_property_sell_listing_id'),
        ForeignKeyConstraint(['service_id'], ['master_service.id'], name='fk_property_sell_listing_service_service_id'),
        PrimaryKeyConstraint('id', name='pk_property_sell_listing_service_id'),
        UniqueConstraint('property_sell_listing_id', 'service_id', name='uq_property_sell_listing_service')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    property_sell_listing_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    service_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))

    property_sell_listing: Mapped['PropertySellListing'] = relationship('PropertySellListing', back_populates='property_sell_listing_service')
    service: Mapped['MasterService'] = relationship('MasterService', back_populates='property_sell_listing_service')


class StudentAcademicFinance(Base):
    __tablename__ = 'student_academic_finance'
    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['student_profile.student_id'], name='fk_student_academic_finance_student_id'),
        PrimaryKeyConstraint('id', name='pk_student_academic_finance_id'),
        UniqueConstraint('student_id', name='uk_student_academic_finance_student_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[str] = mapped_column(String(150), nullable=False)
    father_name: Mapped[Optional[str]] = mapped_column(String(255))
    background: Mapped[Optional[str]] = mapped_column(String(255))
    admission_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    aadhaar_number: Mapped[Optional[str]] = mapped_column(String(150))
    pan_number: Mapped[Optional[str]] = mapped_column(String(150))
    scholarship_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    scholarship_disbursed_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    sgpa: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    attendance_percent: Mapped[Optional[int]] = mapped_column(Integer)
    backlogs: Mapped[Optional[int]] = mapped_column(Integer)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    student: Mapped['StudentProfile'] = relationship('StudentProfile', back_populates='student_academic_finance')


class StudentFeeInstallments(Base):
    __tablename__ = 'student_fee_installments'
    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['student_profile.student_id'], name='fk_student_fee_installments_student_id'),
        PrimaryKeyConstraint('id', name='pk_student_fee_installments_id'),
        UniqueConstraint('student_id', 'installment_no', name='uk_student_fee_installments')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[str] = mapped_column(String(150), nullable=False)
    installment_no: Mapped[int] = mapped_column(Integer, nullable=False)
    installment_amount: Mapped[decimal.Decimal] = mapped_column(Numeric, nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    paid_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    student: Mapped['StudentProfile'] = relationship('StudentProfile', back_populates='student_fee_installments')


class TaskHistory(Base):
    __tablename__ = 'task_history'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_task_history_rating'),
        ForeignKeyConstraint(['from_assignee_id'], ['user_registration.id'], name='fk_task_history_from_assignee_id'),
        ForeignKeyConstraint(['reporting_manager_id'], ['user_registration.id'], name='fk_task_history_reporting_manager_id'),
        ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_task_history_task_id'),
        ForeignKeyConstraint(['to_assignee_id'], ['user_registration.id'], name='fk_task_history_to_assignee_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_task_history_user_id'),
        PrimaryKeyConstraint('id', name='pk_task_history_id'),
        Index('idx_task_history_from_assignee_id', 'from_assignee_id'),
        Index('idx_task_history_reporting_manager_id', 'reporting_manager_id'),
        Index('idx_task_history_task_id', 'task_id'),
        Index('idx_task_history_to_assignee_id', 'to_assignee_id'),
        Index('idx_task_history_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    task_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    from_assignee_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    to_assignee_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    reporting_manager_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    comments: Mapped[Optional[str]] = mapped_column(String)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    from_assignee: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[from_assignee_id], back_populates='task_history')
    reporting_manager: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[reporting_manager_id], back_populates='task_history_')
    task: Mapped['Tasks'] = relationship('Tasks', back_populates='task_history')
    to_assignee: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[to_assignee_id], back_populates='task_history1')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='task_history2')


class VehicleBrandFuel(Base):
    __tablename__ = 'vehicle_brand_fuel'
    __table_args__ = (
        ForeignKeyConstraint(['brand_id'], ['master_vehicle_brand.id'], name='fk_vehicle_brand_fuel_brand_id'),
        ForeignKeyConstraint(['fuel_id'], ['master_fuel_type.id'], name='fk_vehicle_brand_fuel_fuel_id'),
        ForeignKeyConstraint(['sub_service_id'], ['master_sub_service.id'], name='fk_vehicle_brand_fuel_sub_service_id'),
        PrimaryKeyConstraint('id', name='pk_vehicle_brand_fuel_id'),
        UniqueConstraint('sub_service_id', 'brand_id', 'fuel_id', name='uk_vehicle_brand_fuel')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_service_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    brand_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    fuel_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    brand: Mapped['MasterVehicleBrand'] = relationship('MasterVehicleBrand', back_populates='vehicle_brand_fuel')
    fuel: Mapped['MasterFuelType'] = relationship('MasterFuelType', back_populates='vehicle_brand_fuel')
    sub_service: Mapped['MasterSubService'] = relationship('MasterSubService', back_populates='vehicle_brand_fuel')


class AmbulanceBooking(Base):
    __tablename__ = 'ambulance_booking'
    __table_args__ = (
        ForeignKeyConstraint(['ambulance_id'], ['master_ambulance.id'], name='fk_ambulance_booking_ambulance'),
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], name='fk_ambulance_booking_appointment'),
        PrimaryKeyConstraint('id', name='pk_ambulance_booking_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    appointment_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ambulance_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    patient_name: Mapped[Optional[str]] = mapped_column(String(255))
    aadhar_number: Mapped[Optional[str]] = mapped_column(String(50))

    ambulance: Mapped['MasterAmbulance'] = relationship('MasterAmbulance', back_populates='ambulance_booking')
    appointment: Mapped['Appointments'] = relationship('Appointments', back_populates='ambulance_booking')


class FreelancerTaskHistory(Base):
    __tablename__ = 'freelancer_task_history'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_freelancer_task_history_rating'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_freelancer_task_history_created_by'),
        ForeignKeyConstraint(['freelancer_id'], ['master_role.id'], name='fk_freelancer_task_history_home_freelancer_id'),
        ForeignKeyConstraint(['home_service_id'], ['home_service.id'], name='fk_freelancer_task_history_home_service_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_freelancer_task_history_modified_by'),
        ForeignKeyConstraint(['work_status_id'], ['master_work_status.id'], name='fk_freelancer_task_history_home_work_status_id'),
        PrimaryKeyConstraint('id', name='pk_freelancer_task_history_id'),
        Index('idx_freelancer_task_history_created_by', 'created_by'),
        Index('idx_freelancer_task_history_freelancer_id', 'freelancer_id'),
        Index('idx_freelancer_task_history_home_service_id', 'home_service_id'),
        Index('idx_freelancer_task_history_modified_by', 'modified_by'),
        Index('idx_freelancer_task_history_work_status_id', 'work_status_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    home_service_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    freelancer_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    work_status_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    upload_img: Mapped[Optional[str]] = mapped_column(String(500))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='freelancer_task_history')
    freelancer: Mapped['MasterRole'] = relationship('MasterRole', back_populates='freelancer_task_history')
    home_service: Mapped['HomeService'] = relationship('HomeService', back_populates='freelancer_task_history')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='freelancer_task_history_')
    work_status: Mapped['MasterWorkStatus'] = relationship('MasterWorkStatus', back_populates='freelancer_task_history')


class HsAddOn(Base):
    __tablename__ = 'hs_add_on'
    __table_args__ = (
        ForeignKeyConstraint(['add_on_id'], ['master_add_on.id'], name='fk_hs_add_on_add_on_id'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_hs_add_on_created_by'),
        ForeignKeyConstraint(['duration_id'], ['master_duration.id'], name='fk_hs_add_on_duration_id'),
        ForeignKeyConstraint(['home_service_id'], ['home_service.id'], name='fk_hs_add_on_home_service_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_hs_add_on_modified_by'),
        PrimaryKeyConstraint('id', name='pk_hs_add_on_id'),
        Index('idx_hs_add_on_add_on_id', 'add_on_id'),
        Index('idx_hs_add_on_created_by', 'created_by'),
        Index('idx_hs_add_on_duration_id', 'duration_id'),
        Index('idx_hs_add_on_home_service_id', 'home_service_id'),
        Index('idx_hs_add_on_modified_by', 'modified_by')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    home_service_id: Mapped[int] = mapped_column(Integer, nullable=False)
    add_on_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    duration_id: Mapped[Optional[int]] = mapped_column(Integer)

    add_on: Mapped['MasterAddOn'] = relationship('MasterAddOn', back_populates='hs_add_on')
    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='hs_add_on')
    duration: Mapped[Optional['MasterDuration']] = relationship('MasterDuration', back_populates='hs_add_on')
    home_service: Mapped['HomeService'] = relationship('HomeService', back_populates='hs_add_on')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='hs_add_on_')


class MasterMechanic(Base):
    __tablename__ = 'master_mechanic'
    __table_args__ = (
        ForeignKeyConstraint(['garage_id'], ['master_garage.id'], name='fk_master_mechanic_garage_id'),
        PrimaryKeyConstraint('id', name='pk_master_mechanic_id'),
        UniqueConstraint('garage_id', 'mechanic_name', name='uk_master_mechanic_name_garage')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    garage_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    mechanic_name: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(2, 1))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    garage: Mapped['MasterGarage'] = relationship('MasterGarage', back_populates='master_mechanic')
    vehicle_service_booking: Mapped[list['VehicleServiceBooking']] = relationship('VehicleServiceBooking', back_populates='mechanic')


class VehicleServiceBooking(Base):
    __tablename__ = 'vehicle_service_booking'
    __table_args__ = (
        ForeignKeyConstraint(['brand_id'], ['master_vehicle_brand.id'], name='fk_vehicle_service_booking_brand_id'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_vehicle_service_booking_created_by'),
        ForeignKeyConstraint(['fuel_id'], ['master_fuel_type.id'], name='fk_vehicle_service_booking_fuel_id'),
        ForeignKeyConstraint(['garage_id'], ['master_garage.id'], name='fk_vehicle_service_booking_garage_id'),
        ForeignKeyConstraint(['mechanic_id'], ['master_mechanic.id'], name='fk_vehicle_service_booking_mechanic_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_vehicle_service_booking_modified_by'),
        ForeignKeyConstraint(['sub_service_id'], ['master_sub_service.id'], name='fk_vehicle_service_booking_sub_service_id'),
        ForeignKeyConstraint(['time_slot_id'], ['master_time_slot.id'], name='fk_vehicle_service_booking_time_slot_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_vehicle_service_booking_user_id'),
        PrimaryKeyConstraint('id', name='pk_vehicle_service_booking_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sub_service_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    brand_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    fuel_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    garage_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    mechanic_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    problem_description: Mapped[Optional[str]] = mapped_column(String(500))
    address: Mapped[Optional[str]] = mapped_column(String(500))
    customer_name: Mapped[Optional[str]] = mapped_column(String(255))
    contact_number: Mapped[Optional[str]] = mapped_column(String(255))
    preferred_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    time_slot_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    image_urls: Mapped[Optional[str]] = mapped_column(String(500))
    items_total: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    garage_base_fee: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    final_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    brand: Mapped['MasterVehicleBrand'] = relationship('MasterVehicleBrand', back_populates='vehicle_service_booking')
    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='vehicle_service_booking')
    fuel: Mapped['MasterFuelType'] = relationship('MasterFuelType', back_populates='vehicle_service_booking')
    garage: Mapped['MasterGarage'] = relationship('MasterGarage', back_populates='vehicle_service_booking')
    mechanic: Mapped[Optional['MasterMechanic']] = relationship('MasterMechanic', back_populates='vehicle_service_booking')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='vehicle_service_booking_')
    sub_service: Mapped['MasterSubService'] = relationship('MasterSubService', back_populates='vehicle_service_booking')
    time_slot: Mapped[Optional['MasterTimeSlot']] = relationship('MasterTimeSlot', back_populates='vehicle_service_booking')
    user: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='vehicle_service_booking1')
    booking_service_mapping: Mapped[list['BookingServiceMapping']] = relationship('BookingServiceMapping', back_populates='booking')


class BookingServiceMapping(Base):
    __tablename__ = 'booking_service_mapping'
    __table_args__ = (
        ForeignKeyConstraint(['booking_id'], ['vehicle_service_booking.id'], name='fk_booking_service_mapping_booking_id'),
        ForeignKeyConstraint(['garage_service_id'], ['master_garage_service.id'], name='fk_booking_service_mapping_garage_service_id'),
        PrimaryKeyConstraint('id', name='pk_booking_service_mapping_id'),
        UniqueConstraint('booking_id', 'garage_service_id', name='uq_booking_service')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    booking_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    garage_service_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    quantity: Mapped[Optional[int]] = mapped_column(Integer)
    service_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    booking: Mapped['VehicleServiceBooking'] = relationship('VehicleServiceBooking', back_populates='booking_service_mapping')
    garage_service: Mapped['MasterGarageService'] = relationship('MasterGarageService', back_populates='booking_service_mapping')
