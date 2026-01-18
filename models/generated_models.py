from typing import Optional
import datetime
import decimal

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Date, DateTime, ForeignKeyConstraint, Index, Integer, JSON, Numeric, PrimaryKeyConstraint, String, UniqueConstraint, text
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


class MasterApprovalType(Base):
    __tablename__ = 'master_approval_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_approval_type_id'),
        UniqueConstraint('approval_type', name='uk_master_approval_type_approval_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    approval_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='approval_type')


class MasterAvailabilityStatus(Base):
    __tablename__ = 'master_availability_status'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_availability_status_id'),
        UniqueConstraint('availability_status', name='uk_master_availability_status_availability_status')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    availability_status: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='availability_status')


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

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='boundary_type')


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
    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='city')


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

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='facing')


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


class MasterLandType(Base):
    __tablename__ = 'master_land_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_land_type_id'),
        UniqueConstraint('land_type', name='uk_master_land_type_land_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    land_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='land_type')


class MasterLeaseType(Base):
    __tablename__ = 'master_lease_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_lease_type_id'),
        UniqueConstraint('lease_type', name='uk_master_lease_type_lease_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lease_type: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='lease_type')


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

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='ownership_type')


class MasterParking(Base):
    __tablename__ = 'master_parking'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_parking_type_id'),
        UniqueConstraint('parking_type', name='uk_master_parking_type_parking_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parking_type: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='parking')


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


class MasterPostedBy(Base):
    __tablename__ = 'master_posted_by'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_posted_by_id'),
        UniqueConstraint('posted_by', name='uk_master_posted_by_posted_by')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    posted_by: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='posted_by')


class MasterPreferredTenants(Base):
    __tablename__ = 'master_preferred_tenants'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_preferred_tenants_id'),
        UniqueConstraint('tenant_type', name='uk_master_preferred_tenants_tenant_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='preferred_tenants')


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
    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='state')


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
    home_service: Mapped[list['HomeService']] = relationship('HomeService', back_populates='status')


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


class JobOpenings(Base):
    __tablename__ = 'job_openings'
    __table_args__ = (
        ForeignKeyConstraint(['job_id'], ['master_job.id'], name='fk_job_openings_job_id'),
        ForeignKeyConstraint(['location_type_id'], ['master_location_type.id'], name='fk_job_openings_location_type_id'),
        ForeignKeyConstraint(['work_type_id'], ['master_work_type.id'], name='fk_job_openings_work_type_id'),
        PrimaryKeyConstraint('id', name='pk_job_openings_id')
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

    job: Mapped['MasterJob'] = relationship('MasterJob', back_populates='job_openings')
    location_type: Mapped['MasterLocationType'] = relationship('MasterLocationType', back_populates='job_openings')
    work_type: Mapped['MasterWorkType'] = relationship('MasterWorkType', back_populates='job_openings')
    job_skill: Mapped[list['JobSkill']] = relationship('JobSkill', back_populates='job_openings')
    job_application: Mapped[list['JobApplication']] = relationship('JobApplication', back_populates='job_openings')


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


class JobSkill(Base):
    __tablename__ = 'job_skill'
    __table_args__ = (
        ForeignKeyConstraint(['job_openings_id'], ['job_openings.id'], name='fk_job_skill_job_openings_id'),
        ForeignKeyConstraint(['skill_id'], ['master_skill.id'], name='fk_job_skill_skill_id'),
        PrimaryKeyConstraint('id', name='pk_job_skill_id')
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


class UserRegistration(Base):
    __tablename__ = 'user_registration'
    __table_args__ = (
        ForeignKeyConstraint(['district_id'], ['master_district.id'], name='fk_user_registration_district_id'),
        ForeignKeyConstraint(['gender_id'], ['master_gender.id'], name='fk_user_registration_gender_id'),
        ForeignKeyConstraint(['role_id'], ['master_role.id'], name='fk_user_registration_role_id'),
        ForeignKeyConstraint(['state_id'], ['master_state.id'], name='fk_user_registration_state_id'),
        ForeignKeyConstraint(['status_id'], ['master_status.id'], name='fk_user_registration_status_id'),
        PrimaryKeyConstraint('id', name='pk_user_registration_id'),
        UniqueConstraint('email', name='uk_user_registration_email'),
        UniqueConstraint('mobile', name='uk_user_registration_mobile'),
        UniqueConstraint('unique_id', name='uk_user_registration_unique_id'),
        Index('idx_user_registration_district_id', 'district_id'),
        Index('idx_user_registration_gender_id', 'gender_id'),
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

    district: Mapped[Optional['MasterDistrict']] = relationship('MasterDistrict', back_populates='user_registration')
    gender: Mapped[Optional['MasterGender']] = relationship('MasterGender', back_populates='user_registration')
    role: Mapped[Optional['MasterRole']] = relationship('MasterRole', back_populates='user_registration')
    state: Mapped[Optional['MasterState']] = relationship('MasterState', back_populates='user_registration')
    status: Mapped[Optional['MasterStatus']] = relationship('MasterStatus', back_populates='user_registration')
    job_application: Mapped[list['JobApplication']] = relationship('JobApplication', back_populates='user')
    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', foreign_keys='[PropertySellListing.created_by]', back_populates='user_registration')
    property_sell_listing_: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', foreign_keys='[PropertySellListing.modified_by]', back_populates='user_registration_')
    student_certificate: Mapped[list['StudentCertificate']] = relationship('StudentCertificate', foreign_keys='[StudentCertificate.created_by]', back_populates='user_registration')
    student_certificate_: Mapped[list['StudentCertificate']] = relationship('StudentCertificate', foreign_keys='[StudentCertificate.modified_by]', back_populates='user_registration_')
    student_certificate1: Mapped[list['StudentCertificate']] = relationship('StudentCertificate', foreign_keys='[StudentCertificate.user_id]', back_populates='user')
    student_qualification: Mapped[list['StudentQualification']] = relationship('StudentQualification', foreign_keys='[StudentQualification.created_by]', back_populates='user_registration')
    student_qualification_: Mapped[list['StudentQualification']] = relationship('StudentQualification', foreign_keys='[StudentQualification.modified_by]', back_populates='user_registration_')
    student_qualification1: Mapped[list['StudentQualification']] = relationship('StudentQualification', foreign_keys='[StudentQualification.user_id]', back_populates='user')
    user_role: Mapped[list['UserRole']] = relationship('UserRole', foreign_keys='[UserRole.created_by]', back_populates='user_registration')
    user_role_: Mapped[list['UserRole']] = relationship('UserRole', foreign_keys='[UserRole.modified_by]', back_populates='user_registration_')
    user_role1: Mapped[list['UserRole']] = relationship('UserRole', foreign_keys='[UserRole.user_id]', back_populates='user')
    user_services: Mapped[list['UserServices']] = relationship('UserServices', foreign_keys='[UserServices.created_by]', back_populates='user_registration')
    user_services_: Mapped[list['UserServices']] = relationship('UserServices', foreign_keys='[UserServices.modified_by]', back_populates='user_registration_')
    user_services1: Mapped[list['UserServices']] = relationship('UserServices', foreign_keys='[UserServices.user_id]', back_populates='user')
    user_skill: Mapped[list['UserSkill']] = relationship('UserSkill', foreign_keys='[UserSkill.created_by]', back_populates='user_registration')
    user_skill_: Mapped[list['UserSkill']] = relationship('UserSkill', foreign_keys='[UserSkill.modified_by]', back_populates='user_registration_')
    user_skill1: Mapped[list['UserSkill']] = relationship('UserSkill', foreign_keys='[UserSkill.user_id]', back_populates='user')
    home_service: Mapped[list['HomeService']] = relationship('HomeService', foreign_keys='[HomeService.assigned_to]', back_populates='user_registration')
    home_service_: Mapped[list['HomeService']] = relationship('HomeService', foreign_keys='[HomeService.created_by]', back_populates='user_registration_')
    home_service1: Mapped[list['HomeService']] = relationship('HomeService', foreign_keys='[HomeService.modified_by]', back_populates='user_registration1')
    property_listing: Mapped[list['PropertyListing']] = relationship('PropertyListing', foreign_keys='[PropertyListing.created_by]', back_populates='user_registration')
    property_listing_: Mapped[list['PropertyListing']] = relationship('PropertyListing', foreign_keys='[PropertyListing.modified_by]', back_populates='user_registration_')
    property_listing1: Mapped[list['PropertyListing']] = relationship('PropertyListing', foreign_keys='[PropertyListing.user_id]', back_populates='user')
    freelancer_task_history: Mapped[list['FreelancerTaskHistory']] = relationship('FreelancerTaskHistory', foreign_keys='[FreelancerTaskHistory.created_by]', back_populates='user_registration')
    freelancer_task_history_: Mapped[list['FreelancerTaskHistory']] = relationship('FreelancerTaskHistory', foreign_keys='[FreelancerTaskHistory.modified_by]', back_populates='user_registration_')
    hs_add_on: Mapped[list['HsAddOn']] = relationship('HsAddOn', foreign_keys='[HsAddOn.created_by]', back_populates='user_registration')
    hs_add_on_: Mapped[list['HsAddOn']] = relationship('HsAddOn', foreign_keys='[HsAddOn.modified_by]', back_populates='user_registration_')


class JobApplication(Base):
    __tablename__ = 'job_application'
    __table_args__ = (
        CheckConstraint('fresher = true AND experienced = false AND company IS NULL AND from_date IS NULL AND to_date IS NULL AND company_city_id IS NULL AND current_ctc IS NULL OR fresher = false AND experienced = true AND company IS NOT NULL AND from_date IS NOT NULL AND to_date IS NOT NULL AND company_city_id IS NOT NULL AND current_ctc IS NOT NULL', name='ck_job_application_fresher_experienced'),
        ForeignKeyConstraint(['city_id'], ['master_city.id'], name='fk_job_application_city_id'),
        ForeignKeyConstraint(['company_city_id'], ['master_city.id'], name='fk_job_application_company_city_id'),
        ForeignKeyConstraint(['job_openings_id'], ['job_openings.id'], name='fk_job_application_job_openings_id'),
        ForeignKeyConstraint(['mobile_code_id'], ['master_mobile_code.id'], name='fk_job_application_mobile_code_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_job_application_user_id'),
        PrimaryKeyConstraint('id', name='pk_job_application_id')
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
    master_sub_group: Mapped[list['MasterSubGroup']] = relationship('MasterSubGroup', back_populates='sub_service')


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


class PropertySellListing(Base):
    __tablename__ = 'property_sell_listing'
    __table_args__ = (
        ForeignKeyConstraint(['approval_type_id'], ['master_approval_type.id'], name='fk_property_sell_listing_approval_type_id'),
        ForeignKeyConstraint(['availability_status_id'], ['master_availability_status.id'], name='fk_property_sell_listing_availability_status_id'),
        ForeignKeyConstraint(['bhk_type_id'], ['master_bhk_type.id'], name='fk_property_sell_listing_bhk_type_id'),
        ForeignKeyConstraint(['boundary_type_id'], ['master_boundary_type.id'], name='fk_property_sell_listing_boundary_type_id'),
        ForeignKeyConstraint(['city_id'], ['master_city.id'], name='fk_property_sell_listing_city_id'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_property_sell_listing_created_by'),
        ForeignKeyConstraint(['facing_id'], ['master_facing.id'], name='fk_property_sell_listing_facing_id'),
        ForeignKeyConstraint(['furnishing_id'], ['master_furnishing.id'], name='fk_property_sell_listing_furnishing_id'),
        ForeignKeyConstraint(['land_type_id'], ['master_land_type.id'], name='fk_property_sell_listing_land_type_id'),
        ForeignKeyConstraint(['lease_type_id'], ['master_lease_type.id'], name='fk_property_sell_listing_lease_type_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_property_sell_listing_modified_by'),
        ForeignKeyConstraint(['module_id'], ['master_module.id'], name='fk_property_sell_listing_module_id'),
        ForeignKeyConstraint(['ownership_type_id'], ['master_ownership_type.id'], name='fk_property_sell_listing_ownership_type_id'),
        ForeignKeyConstraint(['parking_id'], ['master_parking.id'], name='fk_property_sell_listing_parking_id'),
        ForeignKeyConstraint(['posted_by_id'], ['master_posted_by.id'], name='fk_property_sell_listing_posted_by_id'),
        ForeignKeyConstraint(['preferred_tenants_id'], ['master_preferred_tenants.id'], name='fk_property_sell_listing_preferred_tenants_id'),
        ForeignKeyConstraint(['property_type_id'], ['master_property_type.id'], name='fk_property_sell_listing_property_type_id'),
        ForeignKeyConstraint(['state_id'], ['master_state.id'], name='fk_property_sell_listing_state_id'),
        ForeignKeyConstraint(['sub_module_id'], ['master_sub_module.id'], name='fk_property_sell_listing_sub_module_id'),
        PrimaryKeyConstraint('id', name='pk_property_sell_listing')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sub_module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    bhk_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    furnishing_id: Mapped[int] = mapped_column(Integer, nullable=False)
    parking_id: Mapped[int] = mapped_column(Integer, nullable=False)
    city_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    locality_area: Mapped[str] = mapped_column(String(255), nullable=False)
    landmark: Mapped[str] = mapped_column(String(255), nullable=False)
    pincode: Mapped[int] = mapped_column(Integer, nullable=False)
    upload_photos: Mapped[str] = mapped_column(String(500), nullable=False)
    owner_name: Mapped[str] = mapped_column(String(255), nullable=False)
    mobile_number: Mapped[str] = mapped_column(String(255), nullable=False)
    property_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    land_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    plot_area: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    length_breadth: Mapped[Optional[str]] = mapped_column(String(255))
    facing_id: Mapped[Optional[int]] = mapped_column(Integer)
    road_width: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    boundary_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    water_availability: Mapped[Optional[bool]] = mapped_column(Boolean)
    electricity_connection: Mapped[Optional[bool]] = mapped_column(Boolean)
    approval_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    ownership_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    expected_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    negotiable: Mapped[Optional[bool]] = mapped_column(Boolean)
    road_access: Mapped[Optional[str]] = mapped_column(String(255))
    suitable_for: Mapped[Optional[str]] = mapped_column(String(255))
    warehouse: Mapped[Optional[str]] = mapped_column(String(255))
    monthly_rent: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    lease_duration: Mapped[Optional[str]] = mapped_column(String(255))
    security_deposit: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    available_from: Mapped[Optional[datetime.date]] = mapped_column(Date)
    built_up_area: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    carpet_area: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    floor_number: Mapped[Optional[int]] = mapped_column(Integer)
    total_floors: Mapped[Optional[int]] = mapped_column(Integer)
    property_age: Mapped[Optional[int]] = mapped_column(Integer)
    preferred_tenants_id: Mapped[Optional[int]] = mapped_column(Integer)
    bathrooms: Mapped[Optional[int]] = mapped_column(Integer)
    maintenance_charges: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    balconies: Mapped[Optional[int]] = mapped_column(Integer)
    lease_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    availability_status_id: Mapped[Optional[int]] = mapped_column(Integer)
    state_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    upload_videos: Mapped[Optional[str]] = mapped_column(String(500))
    property_description: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    best_time_to_call: Mapped[Optional[str]] = mapped_column(String(255))
    posted_by_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    approval_type: Mapped[Optional['MasterApprovalType']] = relationship('MasterApprovalType', back_populates='property_sell_listing')
    availability_status: Mapped[Optional['MasterAvailabilityStatus']] = relationship('MasterAvailabilityStatus', back_populates='property_sell_listing')
    bhk_type: Mapped['MasterBhkType'] = relationship('MasterBhkType', back_populates='property_sell_listing')
    boundary_type: Mapped[Optional['MasterBoundaryType']] = relationship('MasterBoundaryType', back_populates='property_sell_listing')
    city: Mapped['MasterCity'] = relationship('MasterCity', back_populates='property_sell_listing')
    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='property_sell_listing')
    facing: Mapped[Optional['MasterFacing']] = relationship('MasterFacing', back_populates='property_sell_listing')
    furnishing: Mapped['MasterFurnishing'] = relationship('MasterFurnishing', back_populates='property_sell_listing')
    land_type: Mapped[Optional['MasterLandType']] = relationship('MasterLandType', back_populates='property_sell_listing')
    lease_type: Mapped[Optional['MasterLeaseType']] = relationship('MasterLeaseType', back_populates='property_sell_listing')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='property_sell_listing_')
    module: Mapped['MasterModule'] = relationship('MasterModule', back_populates='property_sell_listing')
    ownership_type: Mapped[Optional['MasterOwnershipType']] = relationship('MasterOwnershipType', back_populates='property_sell_listing')
    parking: Mapped['MasterParking'] = relationship('MasterParking', back_populates='property_sell_listing')
    posted_by: Mapped[Optional['MasterPostedBy']] = relationship('MasterPostedBy', back_populates='property_sell_listing')
    preferred_tenants: Mapped[Optional['MasterPreferredTenants']] = relationship('MasterPreferredTenants', back_populates='property_sell_listing')
    property_type: Mapped[Optional['MasterPropertyType']] = relationship('MasterPropertyType', back_populates='property_sell_listing')
    state: Mapped[Optional['MasterState']] = relationship('MasterState', back_populates='property_sell_listing')
    sub_module: Mapped['MasterSubModule'] = relationship('MasterSubModule', back_populates='property_sell_listing')
    property_listing: Mapped[list['PropertyListing']] = relationship('PropertyListing', back_populates='property_sell_listing')


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
        Index('idx_home_service_time_slot_id', 'time_slot_id')
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
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_property_listing_created_by'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_property_listing_modified_by'),
        ForeignKeyConstraint(['property_sell_listing_id'], ['property_sell_listing.id'], name='fk_property_listing_property_sell_listing_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_property_listing_user_id'),
        PrimaryKeyConstraint('id', name='pk_property_listing_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    property_sell_listing_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='property_listing')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='property_listing_')
    property_sell_listing: Mapped['PropertySellListing'] = relationship('PropertySellListing', back_populates='property_listing')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='property_listing1')


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
