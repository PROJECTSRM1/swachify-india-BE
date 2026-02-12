from typing import Any, Optional
import datetime
import decimal

from pgvector.sqlalchemy.vector import VECTOR
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, ForeignKeyConstraint, Index, Integer, JSON, Numeric, PrimaryKeyConstraint, Sequence, String, Table, Text, Time, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class AiDocuments(Base):
    __tablename__ = 'ai_documents'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_documents_id'),
        UniqueConstraint('doc_id', 'chunk_id', name='uk_documents_doc_chunk'),
        Index('ai_documents_embedding_idx', 'embedding')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    doc_id: Mapped[str] = mapped_column(String(150), nullable=False)
    chunk_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    embedding: Mapped[Any] = mapped_column(VECTOR(384), nullable=False)
    language: Mapped[Optional[str]] = mapped_column(String(50))
    metadata_: Mapped[Optional[dict]] = mapped_column('metadata', JSONB)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class AvailablePharmacies(Base):
    __tablename__ = 'available_pharmacies'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_master_pharmacies_rating'),
        PrimaryKeyConstraint('id', name='pk_master_pharmacies_id'),
        UniqueConstraint('pharmacy_name', name='master_pharmacies_pharmacy_name_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, Sequence('master_pharmacies_id_seq'), primary_key=True)
    pharmacy_name: Mapped[str] = mapped_column(String(255), nullable=False)
    pharmacy_type: Mapped[Optional[str]] = mapped_column(String(100))
    services: Mapped[Optional[str]] = mapped_column(String(255))
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    delivery_time: Mapped[Optional[str]] = mapped_column(String(50))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    upload_prescription: Mapped[Optional[str]] = mapped_column(String(500))
    proceed_type: Mapped[Optional[str]] = mapped_column(String(255))
    delivery_address: Mapped[Optional[str]] = mapped_column(String(255))
    special_instructions: Mapped[Optional[str]] = mapped_column(String(255))
    open_from: Mapped[Optional[datetime.time]] = mapped_column(Time)
    open_to: Mapped[Optional[datetime.time]] = mapped_column(Time)
    home_delivery: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    service_requests: Mapped[list['ServiceRequests']] = relationship('ServiceRequests', back_populates='pharmacy')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='pharmacies')


class BusFleet(Base):
    __tablename__ = 'bus_fleet'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_bus_fleet_id'),
        UniqueConstraint('bus_id', name='uk_bus_fleet_bus_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    bus_id: Mapped[str] = mapped_column(String(20), nullable=False)
    bus_name: Mapped[Optional[str]] = mapped_column(String(100))
    driver_name: Mapped[Optional[str]] = mapped_column(String(100))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    bus_alert_log: Mapped[list['BusAlertLog']] = relationship('BusAlertLog', back_populates='bus')
    bus_tracking_status: Mapped[list['BusTrackingStatus']] = relationship('BusTrackingStatus', back_populates='bus')


class HomeServiceBooking(Base):
    __tablename__ = 'home_service_booking'
    __table_args__ = (
        ForeignKeyConstraint(['bhk_type_id'], ['master_bhk_type.id'], name='fk_booking_bhk_type_id'),
        ForeignKeyConstraint(['brand_id'], ['master_vehicle_brand.id'], name='fk_booking_brand_id'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_booking_created_by'),
        ForeignKeyConstraint(['fuel_id'], ['master_fuel_type.id'], name='fk_booking_fuel_id'),
        ForeignKeyConstraint(['garage_id'], ['master_garage.id'], name='fk_booking_garage_id'),
        ForeignKeyConstraint(['garage_service_id'], ['master_garage_service.id'], name='fk_booking_garage_service_id'),
        ForeignKeyConstraint(['home_service_payment_id'], ['home_service_payment.id'], name='fk_booking_payment_id'),
        ForeignKeyConstraint(['mechanic_id'], ['master_mechanic.id'], name='fk_booking_mechanic_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_booking_modified_by'),
        ForeignKeyConstraint(['module_id'], ['master_module.id'], name='fk_booking_module_id'),
        ForeignKeyConstraint(['service_id'], ['master_service.id'], name='fk_booking_service_id'),
        ForeignKeyConstraint(['status_id'], ['master_status.id'], name='fk_booking_status_id'),
        ForeignKeyConstraint(['sub_module_id'], ['master_sub_module.id'], name='fk_booking_sub_module_id'),
        ForeignKeyConstraint(['sub_service_id'], ['master_sub_service.id'], name='fk_booking_sub_service_id'),
        ForeignKeyConstraint(['time_slot_id'], ['master_time_slot.id'], name='fk_booking_time_slot_id'),
        PrimaryKeyConstraint('id', name='pk_home_service_booking_id'),
        UniqueConstraint('sub_service_id', 'brand_id', 'fuel_id', 'garage_id', 'garage_service_id', 'mechanic_id', name='uq_booking_vehicle_combo')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sub_module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    service_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sub_service_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    mobile: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    preferred_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    service_summary: Mapped[dict] = mapped_column(JSONB, nullable=False)
    total_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    others_address: Mapped[Optional[str]] = mapped_column(String(255))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    time_slot_id: Mapped[Optional[int]] = mapped_column(Integer)
    extra_hours: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    bhk_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    brand_id: Mapped[Optional[int]] = mapped_column(Integer)
    fuel_id: Mapped[Optional[int]] = mapped_column(Integer)
    garage_id: Mapped[Optional[int]] = mapped_column(Integer)
    garage_service_id: Mapped[Optional[int]] = mapped_column(Integer)
    mechanic_id: Mapped[Optional[int]] = mapped_column(Integer)
    special_instructions: Mapped[Optional[str]] = mapped_column(String(500))
    upload_photos: Mapped[Optional[str]] = mapped_column(String(500))
    payment_done: Mapped[Optional[bool]] = mapped_column(Boolean)
    status_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    convenience_fee: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2), server_default=text('0'))
    home_service_payment_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    item_total: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2), server_default=text('0'))

    bhk_type: Mapped[Optional['MasterBhkType']] = relationship('MasterBhkType', back_populates='home_service_booking')
    brand: Mapped[Optional['MasterVehicleBrand']] = relationship('MasterVehicleBrand', back_populates='home_service_booking')
    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='home_service_booking')
    fuel: Mapped[Optional['MasterFuelType']] = relationship('MasterFuelType', back_populates='home_service_booking')
    garage: Mapped[Optional['MasterGarage']] = relationship('MasterGarage', back_populates='home_service_booking')
    garage_service: Mapped[Optional['MasterGarageService']] = relationship('MasterGarageService', back_populates='home_service_booking')
    home_service_payment: Mapped[Optional['HomeServicePayment']] = relationship('HomeServicePayment', foreign_keys=[home_service_payment_id], back_populates='home_service_booking')
    mechanic: Mapped[Optional['MasterMechanic']] = relationship('MasterMechanic', back_populates='home_service_booking')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='home_service_booking_')
    module: Mapped['MasterModule'] = relationship('MasterModule', back_populates='home_service_booking')
    service: Mapped['MasterService'] = relationship('MasterService', back_populates='home_service_booking')
    status: Mapped[Optional['MasterStatus']] = relationship('MasterStatus', back_populates='home_service_booking')
    sub_module: Mapped['MasterSubModule'] = relationship('MasterSubModule', back_populates='home_service_booking')
    sub_service: Mapped['MasterSubService'] = relationship('MasterSubService', back_populates='home_service_booking')
    time_slot: Mapped[Optional['MasterTimeSlot']] = relationship('MasterTimeSlot', back_populates='home_service_booking')
    home_service_payment_: Mapped[list['HomeServicePayment']] = relationship('HomeServicePayment', foreign_keys='[HomeServicePayment.booking_id]', back_populates='booking')
    home_service_booking_add_on: Mapped[list['HomeServiceBookingAddOn']] = relationship('HomeServiceBookingAddOn', back_populates='home_service_booking')
    home_service_booking_service_map: Mapped[list['HomeServiceBookingServiceMap']] = relationship('HomeServiceBookingServiceMap', back_populates='home_service_booking')


class HomeServicePayment(Base):
    __tablename__ = 'home_service_payment'
    __table_args__ = (
        ForeignKeyConstraint(['booking_id'], ['home_service_booking.id'], name='fk_payment_booking_id'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_payment_created_by'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_payment_modified_by'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_payment_user_id'),
        PrimaryKeyConstraint('id', name='pk_home_service_payment_id'),
        UniqueConstraint('transaction_id', name='uk_home_service_payment_transaction_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    booking_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    item_total: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_paid: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_mode: Mapped[Optional[str]] = mapped_column(String(100))
    payment_gateway: Mapped[Optional[str]] = mapped_column(String(100))
    transaction_id: Mapped[Optional[str]] = mapped_column(String(255))
    convenience_fee: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2), server_default=text('0'))
    payment_status: Mapped[Optional[str]] = mapped_column(String(50))
    payment_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', foreign_keys='[HomeServiceBooking.home_service_payment_id]', back_populates='home_service_payment')
    booking: Mapped['HomeServiceBooking'] = relationship('HomeServiceBooking', foreign_keys=[booking_id], back_populates='home_service_payment_')
    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='home_service_payment')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='home_service_payment_')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='home_service_payment1')


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
    bhk_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='bhk_type')
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


class MasterConsultationType(Base):
    __tablename__ = 'master_consultation_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_consultation_type_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consultation_type: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    doctor_profile: Mapped[list['DoctorProfile']] = relationship('DoctorProfile', back_populates='consultation_type')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='consultation_type')


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

    home_service_booking_add_on: Mapped[list['HomeServiceBookingAddOn']] = relationship('HomeServiceBookingAddOn', back_populates='duration')


class MasterFacility(Base):
    __tablename__ = 'master_facility'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_facility_id'),
        UniqueConstraint('facility_name', name='uk_master_facility')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    facility_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    master_property_type_facilities: Mapped[list['MasterPropertyTypeFacilities']] = relationship('MasterPropertyTypeFacilities', back_populates='facility')


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

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='fuel')
    vehicle_brand_fuel: Mapped[list['VehicleBrandFuel']] = relationship('VehicleBrandFuel', back_populates='fuel')


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
        CheckConstraint('rating >= 1::numeric AND rating <= 5::numeric', name='ck_master_hospital_rating'),
        PrimaryKeyConstraint('id', name='pk_master_hospital_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    hospital_name: Mapped[str] = mapped_column(String(255), nullable=False)
    specialty_type: Mapped[Optional[str]] = mapped_column(String(50))
    location: Mapped[Optional[str]] = mapped_column(String(255))
    contact_number: Mapped[Optional[str]] = mapped_column(String(20))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    timing_from: Mapped[Optional[datetime.time]] = mapped_column(Time)
    timing_to: Mapped[Optional[datetime.time]] = mapped_column(Time)
    is_24x7: Mapped[Optional[bool]] = mapped_column(Boolean)
    next_open: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    rating: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))

    master_ambulance: Mapped[list['MasterAmbulance']] = relationship('MasterAmbulance', back_populates='hospital')
    master_assistants: Mapped[list['MasterAssistants']] = relationship('MasterAssistants', back_populates='hospital')
    doctor_profile: Mapped[list['DoctorProfile']] = relationship('DoctorProfile', back_populates='hospital')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='hospital')


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


class MasterLabSpecialization(Base):
    __tablename__ = 'master_lab_specialization'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_lab_specialization_id'),
        UniqueConstraint('specialization_name', name='master_lab_specialization_specialization_name_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    specialization_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    available_labs: Mapped[list['AvailableLabs']] = relationship('AvailableLabs', back_populates='specialization')


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

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='module')
    master_sub_module: Mapped[list['MasterSubModule']] = relationship('MasterSubModule', back_populates='module')
    raw_material_details: Mapped[list['RawMaterialDetails']] = relationship('RawMaterialDetails', back_populates='module')
    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='module')
    user_services: Mapped[list['UserServices']] = relationship('UserServices', back_populates='module')


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

    master_property_type_facilities: Mapped[list['MasterPropertyTypeFacilities']] = relationship('MasterPropertyTypeFacilities', back_populates='property_type')
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


class MasterRegistrationStatus(Base):
    __tablename__ = 'master_registration_status'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_registration_status_id'),
        UniqueConstraint('registration_status', name='uk_master_registration_status_registration_status')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    registration_status: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='registration_status')


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
    freelancer_task_history: Mapped[list['FreelancerTaskHistory']] = relationship('FreelancerTaskHistory', back_populates='freelancer')
    user_role: Mapped[list['UserRole']] = relationship('UserRole', back_populates='role')


class MasterRoomType(Base):
    __tablename__ = 'master_room_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_room_type_id'),
        UniqueConstraint('room_type', name='uk_master_room_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_type: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='room_type')


class MasterSharingType(Base):
    __tablename__ = 'master_sharing_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_sharing_type_id'),
        UniqueConstraint('sharing_type', name='uk_master_sharing_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sharing_type: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


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


class MasterStarRating(Base):
    __tablename__ = 'master_star_rating'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_master_star_rating_id'),
        UniqueConstraint('star_value', name='uk_master_star_rating')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    star_value: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='star_rating')


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

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='status')
    user_registration: Mapped[list['UserRegistration']] = relationship('UserRegistration', back_populates='status')
    tasks: Mapped[list['Tasks']] = relationship('Tasks', back_populates='status')


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

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='time_slot')


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


class PayrollPeriod(Base):
    __tablename__ = 'payroll_period'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_payroll_period_id'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    month: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    end_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    salary_earnings: Mapped[list['SalaryEarnings']] = relationship('SalaryEarnings', back_populates='payroll_period')


class PayrollSummary(Base):
    __tablename__ = 'payroll_summary'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_payroll_summary_id'),
        UniqueConstraint('payroll_month', name='payroll_summary_payroll_month_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    payroll_month: Mapped[str] = mapped_column(String(20), nullable=False)
    total_net_disbursement: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2))
    staff_count: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'DISBURSED'::character varying"))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class StaffProfile(Base):
    __tablename__ = 'staff_profile'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_staff_profile_id'),
        UniqueConstraint('staff_id', name='uk_staff_profile_staff_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    staff_id: Mapped[str] = mapped_column(String(50), nullable=False)
    staff_name: Mapped[str] = mapped_column(String(255), nullable=False)
    job_title: Mapped[Optional[str]] = mapped_column(String(255))
    department: Mapped[Optional[str]] = mapped_column(String(100))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    staff_payslip: Mapped[list['StaffPayslip']] = relationship('StaffPayslip', back_populates='staff')
    exam_invigilation_assignment: Mapped[list['ExamInvigilationAssignment']] = relationship('ExamInvigilationAssignment', back_populates='staff')


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


t_vw_home_service_booking_summary = Table(
    'vw_home_service_booking_summary', Base.metadata,
    Column('id', BigInteger),
    Column('full_name', String(255)),
    Column('mobile', String(255)),
    Column('email', String(150)),
    Column('address', String(500)),
    Column('others_address', String(255)),
    Column('preferred_date', Date),
    Column('time_slot_id', Integer),
    Column('extra_hours', Integer),
    Column('special_instructions', String(500)),
    Column('service_summary', JSONB),
    Column('upload_photos', String(500)),
    Column('item_total', Numeric(10, 2)),
    Column('convenience_fee', Numeric(10, 2)),
    Column('total_amount', Numeric(10, 2)),
    Column('payment_done', Boolean),
    Column('status_id', Integer),
    Column('module_name', String(255)),
    Column('sub_module_name', String(255)),
    Column('service_name', String(255)),
    Column('sub_service_name', String(255))
)


t_vw_my_bookings = Table(
    'vw_my_bookings', Base.metadata,
    Column('request_id', BigInteger),
    Column('user_id', BigInteger),
    Column('service_type', String(50)),
    Column('booking_status', String(50)),
    Column('request_date', DateTime),
    Column('appointment_id', BigInteger),
    Column('appointment_time', DateTime),
    Column('appointment_status', String(50)),
    Column('payment_id', BigInteger),
    Column('amount', Numeric(10, 2)),
    Column('payment_method', String(50)),
    Column('payment_status', String(50)),
    Column('transaction_id', String(100)),
    Column('payment_date', DateTime)
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


t_vw_salary_summary = Table(
    'vw_salary_summary', Base.metadata,
    Column('payroll_period_id', BigInteger),
    Column('month', String),
    Column('year', Integer),
    Column('staff_count', Integer),
    Column('status', String),
    Column('basic_salary', Numeric(10, 2)),
    Column('hra', Numeric(10, 2)),
    Column('medical', Numeric(10, 2)),
    Column('conveyance', Numeric(10, 2)),
    Column('gross_earnings', Numeric(12, 2)),
    Column('pf', Numeric(10, 2)),
    Column('professional_tax', Numeric(10, 2)),
    Column('insurance', Numeric(10, 2)),
    Column('total_deduction', Numeric(10, 2)),
    Column('total_net_disbursement', Numeric(12, 2)),
    Column('net_payable', Numeric)
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


t_vw_vehicle_brand_fuel = Table(
    'vw_vehicle_brand_fuel', Base.metadata,
    Column('sub_service_id', BigInteger),
    Column('brand_id', Integer),
    Column('brand_name', String(255)),
    Column('fuel_id', Integer),
    Column('fuel_type_name', String(255))
)


class AvailableLabs(Base):
    __tablename__ = 'available_labs'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_master_labs_rating'),
        ForeignKeyConstraint(['specialization_id'], ['master_lab_specialization.id'], name='fk_available_labs_specialization_id'),
        PrimaryKeyConstraint('id', name='pk_master_labs_id'),
        UniqueConstraint('lab_name', name='master_labs_lab_name_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, Sequence('master_labs_id_seq'), primary_key=True)
    lab_name: Mapped[str] = mapped_column(String(255), nullable=False)
    services: Mapped[Optional[str]] = mapped_column(String(255))
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    home_collection: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 6))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    upload_prescription: Mapped[Optional[str]] = mapped_column(String(500))
    proceed_type: Mapped[Optional[str]] = mapped_column(String(255))
    delivery_address: Mapped[Optional[str]] = mapped_column(String(255))
    special_instructions: Mapped[Optional[str]] = mapped_column(String(255))
    specialization_id: Mapped[Optional[int]] = mapped_column(Integer)
    fees_per_test: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    available_from: Mapped[Optional[datetime.time]] = mapped_column(Time)
    available_to: Mapped[Optional[datetime.time]] = mapped_column(Time)
    estimated_delivery: Mapped[Optional[str]] = mapped_column(String(50))
    is_available: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    specialization: Mapped[Optional['MasterLabSpecialization']] = relationship('MasterLabSpecialization', back_populates='available_labs')
    service_requests: Mapped[list['ServiceRequests']] = relationship('ServiceRequests', back_populates='lab')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='labs')


class BusAlertLog(Base):
    __tablename__ = 'bus_alert_log'
    __table_args__ = (
        ForeignKeyConstraint(['bus_id'], ['bus_fleet.bus_id'], name='fk_bus_alert_log_bus_id'),
        PrimaryKeyConstraint('id', name='pk_bus_alert_log_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    bus_id: Mapped[str] = mapped_column(String(20), nullable=False)
    alert_type: Mapped[Optional[str]] = mapped_column(String(100))
    alert_message: Mapped[Optional[str]] = mapped_column(Text)
    alert_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    resolved: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    bus: Mapped['BusFleet'] = relationship('BusFleet', back_populates='bus_alert_log')


class BusTrackingStatus(Base):
    __tablename__ = 'bus_tracking_status'
    __table_args__ = (
        ForeignKeyConstraint(['bus_id'], ['bus_fleet.bus_id'], name='fk_bus_tracking_status_bus_id'),
        PrimaryKeyConstraint('id', name='pk_bus_tracking_status_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    bus_id: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    location_description: Mapped[Optional[str]] = mapped_column(Text)
    current_speed: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    next_stop: Mapped[Optional[str]] = mapped_column(String(100))
    eta_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    last_updated: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    bus: Mapped['BusFleet'] = relationship('BusFleet', back_populates='bus_tracking_status')


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


class MasterAssistants(Base):
    __tablename__ = 'master_assistants'
    __table_args__ = (
        ForeignKeyConstraint(['hospital_id'], ['master_hospital.id'], name='fk_master_assistants_hospital_id'),
        PrimaryKeyConstraint('id', name='pk_master_assistants_id'),
        UniqueConstraint('name', 'hospital_id', name='uk_master_assistants_name_hospital_id'),
        UniqueConstraint('services', 'hospital_id', 'name', name='uk_master_assistants_service_hospital_id_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cost_per_visit: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    services: Mapped[dict] = mapped_column(JSONB, nullable=False)
    hospital_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    rating: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    role: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'Professional'::character varying"))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    currency: Mapped[Optional[str]] = mapped_column(String(100))

    hospital: Mapped['MasterHospital'] = relationship('MasterHospital', back_populates='master_assistants')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='assistants')


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


class MasterPropertyTypeFacilities(Base):
    __tablename__ = 'master_property_type_facilities'
    __table_args__ = (
        ForeignKeyConstraint(['facility_id'], ['master_facility.id'], name='fk_master_facility_id'),
        ForeignKeyConstraint(['property_type_id'], ['master_property_type.id'], name='fk_master_property_type_id'),
        PrimaryKeyConstraint('id', name='master_property_type_facilities_pkey'),
        UniqueConstraint('property_type_id', 'facility_id', name='uk_master_property_facility')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    facility_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    facility: Mapped['MasterFacility'] = relationship('MasterFacility', back_populates='master_property_type_facilities')
    property_type: Mapped['MasterPropertyType'] = relationship('MasterPropertyType', back_populates='master_property_type_facilities')
    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='property_type_facilities')


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

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='sub_module')
    module: Mapped['MasterModule'] = relationship('MasterModule', back_populates='master_sub_module')
    master_service: Mapped[list['MasterService']] = relationship('MasterService', back_populates='sub_module')
    property_sell_listing: Mapped[list['PropertySellListing']] = relationship('PropertySellListing', back_populates='sub_module')


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


class SalaryEarnings(Base):
    __tablename__ = 'salary_earnings'
    __table_args__ = (
        ForeignKeyConstraint(['payroll_period_id'], ['payroll_period.id'], name='fk_salary_earnings_payroll_period_id'),
        PrimaryKeyConstraint('id', name='pk_salary_earnings_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    payroll_period_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    total_net_disbursement: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_deduction: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    staff_count: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String)
    basic_salary: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    hra: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    medical: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    conveyance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    gross_earnings: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2))
    pf: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    professional_tax: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    insurance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    payroll_period: Mapped['PayrollPeriod'] = relationship('PayrollPeriod', back_populates='salary_earnings')


class StaffPayslip(Base):
    __tablename__ = 'staff_payslip'
    __table_args__ = (
        ForeignKeyConstraint(['staff_id'], ['staff_profile.staff_id'], name='fk_staff_payslip_staff_id'),
        PrimaryKeyConstraint('id', name='pk_staff_payslip_id'),
        UniqueConstraint('staff_id', 'payroll_month', name='uk_staff_payslip')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    staff_id: Mapped[str] = mapped_column(String(50), nullable=False)
    payroll_month: Mapped[str] = mapped_column(String(20), nullable=False)
    payment_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    basic_pay: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    hra: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    medical_allowance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    conveyance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    performance_bonus: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    gross_earnings: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    pf_deduction: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    income_tax: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    professional_tax: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    health_insurance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    total_deductions: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    net_salary: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'DISBURSED'::character varying"))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    staff: Mapped['StaffProfile'] = relationship('StaffProfile', back_populates='staff_payslip')


class InstitutionBranch(Base):
    __tablename__ = 'institution_branch'
    __table_args__ = (
        ForeignKeyConstraint(['institution_id'], ['institution_registration.id'], name='fk_institution_branch_institution_id'),
        PrimaryKeyConstraint('id', name='pk_institution_branch_id'),
        UniqueConstraint('institution_id', 'branch_code', name='uk_institution_branch'),
        UniqueConstraint('institution_id', 'branch_name', name='uq_branch_name_per_institution')
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
    enrollment_status: Mapped[list['EnrollmentStatus']] = relationship('EnrollmentStatus', back_populates='institute')
    exam_schedule: Mapped[list['ExamSchedule']] = relationship('ExamSchedule', back_populates='institution')
    maintenance_budget: Mapped[list['MaintenanceBudget']] = relationship('MaintenanceBudget', back_populates='institute')
    student_profile: Mapped[list['StudentProfile']] = relationship('StudentProfile', back_populates='branch')


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

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='service')
    sub_module: Mapped['MasterSubModule'] = relationship('MasterSubModule', back_populates='master_service')
    master_sub_service: Mapped[list['MasterSubService']] = relationship('MasterSubService', back_populates='service')


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
    unique_id: Mapped[Optional[str]] = mapped_column(String(255))
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

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', foreign_keys='[HomeServiceBooking.created_by]', back_populates='user_registration')
    home_service_booking_: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', foreign_keys='[HomeServiceBooking.modified_by]', back_populates='user_registration_')
    home_service_payment: Mapped[list['HomeServicePayment']] = relationship('HomeServicePayment', foreign_keys='[HomeServicePayment.created_by]', back_populates='user_registration')
    home_service_payment_: Mapped[list['HomeServicePayment']] = relationship('HomeServicePayment', foreign_keys='[HomeServicePayment.modified_by]', back_populates='user_registration_')
    home_service_payment1: Mapped[list['HomeServicePayment']] = relationship('HomeServicePayment', foreign_keys='[HomeServicePayment.user_id]', back_populates='user')
    business_type: Mapped[Optional['MasterBusinessType']] = relationship('MasterBusinessType', back_populates='user_registration')
    district: Mapped[Optional['MasterDistrict']] = relationship('MasterDistrict', back_populates='user_registration')
    gender: Mapped[Optional['MasterGender']] = relationship('MasterGender', back_populates='user_registration')
    job_skill: Mapped[Optional['MasterJobSkill']] = relationship('MasterJobSkill', back_populates='user_registration')
    role: Mapped[Optional['MasterRole']] = relationship('MasterRole', back_populates='user_registration')
    state: Mapped[Optional['MasterState']] = relationship('MasterState', back_populates='user_registration')
    status: Mapped[Optional['MasterStatus']] = relationship('MasterStatus', back_populates='user_registration')
    work_type: Mapped[Optional['MasterWorkType']] = relationship('MasterWorkType', back_populates='user_registration')
    doctor_profile: Mapped['DoctorProfile'] = relationship('DoctorProfile', uselist=False, back_populates='user')
    freelancer_task_history: Mapped[list['FreelancerTaskHistory']] = relationship('FreelancerTaskHistory', foreign_keys='[FreelancerTaskHistory.created_by]', back_populates='user_registration')
    freelancer_task_history_: Mapped[list['FreelancerTaskHistory']] = relationship('FreelancerTaskHistory', foreign_keys='[FreelancerTaskHistory.modified_by]', back_populates='user_registration_')
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
    property_listing: Mapped[list['PropertyListing']] = relationship('PropertyListing', foreign_keys='[PropertyListing.created_by]', back_populates='user_registration')
    property_listing_: Mapped[list['PropertyListing']] = relationship('PropertyListing', foreign_keys='[PropertyListing.modified_by]', back_populates='user_registration_')
    property_listing1: Mapped[list['PropertyListing']] = relationship('PropertyListing', foreign_keys='[PropertyListing.user_id]', back_populates='user')
    service_requests: Mapped[list['ServiceRequests']] = relationship('ServiceRequests', back_populates='user')
    task_history: Mapped[list['TaskHistory']] = relationship('TaskHistory', foreign_keys='[TaskHistory.from_assignee_id]', back_populates='from_assignee')
    task_history_: Mapped[list['TaskHistory']] = relationship('TaskHistory', foreign_keys='[TaskHistory.reporting_manager_id]', back_populates='reporting_manager')
    task_history1: Mapped[list['TaskHistory']] = relationship('TaskHistory', foreign_keys='[TaskHistory.to_assignee_id]', back_populates='to_assignee')
    task_history2: Mapped[list['TaskHistory']] = relationship('TaskHistory', foreign_keys='[TaskHistory.user_id]', back_populates='user')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='user')
    home_service_booking_add_on: Mapped[list['HomeServiceBookingAddOn']] = relationship('HomeServiceBookingAddOn', foreign_keys='[HomeServiceBookingAddOn.created_by]', back_populates='user_registration')
    home_service_booking_add_on_: Mapped[list['HomeServiceBookingAddOn']] = relationship('HomeServiceBookingAddOn', foreign_keys='[HomeServiceBookingAddOn.modified_by]', back_populates='user_registration_')
    home_service_booking_service_map: Mapped[list['HomeServiceBookingServiceMap']] = relationship('HomeServiceBookingServiceMap', foreign_keys='[HomeServiceBookingServiceMap.created_by]', back_populates='user_registration')
    home_service_booking_service_map_: Mapped[list['HomeServiceBookingServiceMap']] = relationship('HomeServiceBookingServiceMap', foreign_keys='[HomeServiceBookingServiceMap.modified_by]', back_populates='user_registration_')
    master_mechanic: Mapped[list['MasterMechanic']] = relationship('MasterMechanic', back_populates='user')
    payments: Mapped[list['Payments']] = relationship('Payments', back_populates='user')


class DoctorProfile(Base):
    __tablename__ = 'doctor_profile'
    __table_args__ = (
        CheckConstraint('rating >= 1::numeric AND rating <= 5::numeric', name='ck_doctor_profile_rating'),
        ForeignKeyConstraint(['consultation_type_id'], ['master_consultation_type.id'], name='doctor_profile_consultation_type_id_fkey'),
        ForeignKeyConstraint(['hospital_id'], ['master_hospital.id'], name='doctor_profile_hospital_id_fkey'),
        ForeignKeyConstraint(['specialization_id'], ['master_doctor_specialization.id'], name='fk_doctor_profile_specialization_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_doctor_profile_user_id'),
        PrimaryKeyConstraint('id', name='pk_doctor_profile_id'),
        UniqueConstraint('user_id', name='uk_doctor_profile_user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    specialization_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    experience_years: Mapped[Optional[int]] = mapped_column(Integer)
    rating: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    fees_per_hour: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    available_from: Mapped[Optional[datetime.time]] = mapped_column(Time)
    available_to: Mapped[Optional[datetime.time]] = mapped_column(Time)
    is_available: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    hospital_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    consultation_type_id: Mapped[Optional[int]] = mapped_column(Integer)

    consultation_type: Mapped[Optional['MasterConsultationType']] = relationship('MasterConsultationType', back_populates='doctor_profile')
    hospital: Mapped[Optional['MasterHospital']] = relationship('MasterHospital', back_populates='doctor_profile')
    specialization: Mapped['MasterDoctorSpecialization'] = relationship('MasterDoctorSpecialization', back_populates='doctor_profile')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='doctor_profile')
    service_requests: Mapped[list['ServiceRequests']] = relationship('ServiceRequests', back_populates='doctor')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='doctor')


class EnrollmentStatus(Base):
    __tablename__ = 'enrollment_status'
    __table_args__ = (
        ForeignKeyConstraint(['institute_id'], ['institution_branch.id'], name='fk_enrollment_status_institute'),
        PrimaryKeyConstraint('id', name='pk_enrollment_status_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    institute_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    total_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    approved_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    last_updated: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    institute: Mapped['InstitutionBranch'] = relationship('InstitutionBranch', back_populates='enrollment_status')


class ExamSchedule(Base):
    __tablename__ = 'exam_schedule'
    __table_args__ = (
        ForeignKeyConstraint(['institution_id'], ['institution_branch.id'], name='fk_exam_schedule_institution_id'),
        PrimaryKeyConstraint('id', name='pk_exam_schedule_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    institution_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    exam_type: Mapped[str] = mapped_column(String(255), nullable=False)
    subject_name: Mapped[str] = mapped_column(String(255), nullable=False)
    exam_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    institution: Mapped['InstitutionBranch'] = relationship('InstitutionBranch', back_populates='exam_schedule')
    exam_invigilation_assignment: Mapped[list['ExamInvigilationAssignment']] = relationship('ExamInvigilationAssignment', back_populates='exam_schedule')
    exam_notification_log: Mapped[list['ExamNotificationLog']] = relationship('ExamNotificationLog', back_populates='exam_schedule')
    exam_reminder_settings: Mapped[list['ExamReminderSettings']] = relationship('ExamReminderSettings', back_populates='exam_schedule')


class FreelancerTaskHistory(Base):
    __tablename__ = 'freelancer_task_history'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_freelancer_task_history_rating'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_freelancer_task_history_created_by'),
        ForeignKeyConstraint(['freelancer_id'], ['master_role.id'], name='fk_freelancer_task_history_home_freelancer_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_freelancer_task_history_modified_by'),
        ForeignKeyConstraint(['work_status_id'], ['master_work_status.id'], name='fk_freelancer_task_history_home_work_status_id'),
        PrimaryKeyConstraint('id', name='pk_freelancer_task_history_id'),
        Index('idx_freelancer_task_history_created_by', 'created_by'),
        Index('idx_freelancer_task_history_freelancer_id', 'freelancer_id'),
        Index('idx_freelancer_task_history_modified_by', 'modified_by'),
        Index('idx_freelancer_task_history_work_status_id', 'work_status_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
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
    home_service_booking_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='freelancer_task_history')
    freelancer: Mapped['MasterRole'] = relationship('MasterRole', back_populates='freelancer_task_history')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='freelancer_task_history_')
    work_status: Mapped['MasterWorkStatus'] = relationship('MasterWorkStatus', back_populates='freelancer_task_history')


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


class MaintenanceBudget(Base):
    __tablename__ = 'maintenance_budget'
    __table_args__ = (
        ForeignKeyConstraint(['institute_id'], ['institution_branch.id'], name='fk_maintenance_budget_institute'),
        PrimaryKeyConstraint('id', name='pk_maintenance_budget_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    institute_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    budget_limit: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    budget_used: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    institute: Mapped['InstitutionBranch'] = relationship('InstitutionBranch', back_populates='maintenance_budget')


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

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='sub_service')
    service: Mapped['MasterService'] = relationship('MasterService', back_populates='master_sub_service')
    master_garage: Mapped[list['MasterGarage']] = relationship('MasterGarage', back_populates='sub_service')
    master_garage_service: Mapped[list['MasterGarageService']] = relationship('MasterGarageService', back_populates='sub_service')
    master_package_add_on: Mapped[list['MasterPackageAddOn']] = relationship('MasterPackageAddOn', back_populates='sub_service')
    master_sub_group: Mapped[list['MasterSubGroup']] = relationship('MasterSubGroup', back_populates='sub_service')
    master_vehicle_brand: Mapped[list['MasterVehicleBrand']] = relationship('MasterVehicleBrand', back_populates='sub_service')
    vehicle_brand_fuel: Mapped[list['VehicleBrandFuel']] = relationship('VehicleBrandFuel', back_populates='sub_service')


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
        ForeignKeyConstraint(['land_type_id'], ['master_land_type.id'], name='property_sell_listing_land_type_id'),
        ForeignKeyConstraint(['listing_type_id'], ['master_listing_type.id'], name='fk_property_sell_listing_listing_type_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_property_sell_listing_modified_by'),
        ForeignKeyConstraint(['module_id'], ['master_module.id'], name='fk_property_sell_listing_module_id'),
        ForeignKeyConstraint(['property_type_facilities_id'], ['master_property_type_facilities.id'], name='fk_property_sell_listing_property_type_facilities_id'),
        ForeignKeyConstraint(['property_type_id'], ['master_property_type.id'], name='fk_property_sell_listing_property_type_id'),
        ForeignKeyConstraint(['registration_status_id'], ['master_registration_status.id'], name='property_sell_listing_registration_status_id'),
        ForeignKeyConstraint(['room_type_id'], ['master_room_type.id'], name='property_sell_listing_room_type_id'),
        ForeignKeyConstraint(['star_rating_id'], ['master_star_rating.id'], name='property_sell_listing_star_rating_id'),
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
    sub_module_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    property_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    expected_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    monthly_rent: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    bhk_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    furnishing_id: Mapped[Optional[int]] = mapped_column(Integer)
    locality_area: Mapped[Optional[str]] = mapped_column(String(255))
    upload_photos: Mapped[Optional[str]] = mapped_column(Text)
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
    rooms_per_floor: Mapped[Optional[int]] = mapped_column(Integer)
    beds_per_room: Mapped[Optional[int]] = mapped_column(Integer)
    sharing_type: Mapped[Optional[int]] = mapped_column(Integer)
    current_bill_excluded: Mapped[Optional[bool]] = mapped_column(Boolean)
    band_name: Mapped[Optional[str]] = mapped_column(String(255))
    model_name: Mapped[Optional[str]] = mapped_column(String(255))
    year: Mapped[Optional[int]] = mapped_column(Integer)
    distance_km: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 2))
    owner_name: Mapped[Optional[str]] = mapped_column(String(255))
    mobile_number: Mapped[Optional[str]] = mapped_column(String(255))
    registration_status_id: Mapped[Optional[int]] = mapped_column(Integer)
    registration_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 2))
    land_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    upload_document: Mapped[Optional[str]] = mapped_column(String(500))
    price_per_night: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(9, 2))
    hotel_name: Mapped[Optional[str]] = mapped_column(String(255))
    star_rating_id: Mapped[Optional[int]] = mapped_column(Integer)
    check_in_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    check_out_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    room_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    property_type_facilities_id: Mapped[Optional[int]] = mapped_column(Integer)

    bhk_type: Mapped[Optional['MasterBhkType']] = relationship('MasterBhkType', back_populates='property_sell_listing')
    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='property_sell_listing')
    furnishing: Mapped[Optional['MasterFurnishing']] = relationship('MasterFurnishing', back_populates='property_sell_listing')
    hostel_type: Mapped[Optional['MasterHostelType']] = relationship('MasterHostelType', back_populates='property_sell_listing')
    item_condition: Mapped[Optional['MasterItemCondition']] = relationship('MasterItemCondition', back_populates='property_sell_listing')
    land_type: Mapped[Optional['MasterLandType']] = relationship('MasterLandType', back_populates='property_sell_listing')
    listing_type: Mapped[Optional['MasterListingType']] = relationship('MasterListingType', back_populates='property_sell_listing')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='property_sell_listing_')
    module: Mapped['MasterModule'] = relationship('MasterModule', back_populates='property_sell_listing')
    property_type_facilities: Mapped[Optional['MasterPropertyTypeFacilities']] = relationship('MasterPropertyTypeFacilities', back_populates='property_sell_listing')
    property_type: Mapped[Optional['MasterPropertyType']] = relationship('MasterPropertyType', back_populates='property_sell_listing')
    registration_status: Mapped[Optional['MasterRegistrationStatus']] = relationship('MasterRegistrationStatus', back_populates='property_sell_listing')
    room_type: Mapped[Optional['MasterRoomType']] = relationship('MasterRoomType', back_populates='property_sell_listing')
    star_rating: Mapped[Optional['MasterStarRating']] = relationship('MasterStarRating', back_populates='property_sell_listing')
    sub_module: Mapped[Optional['MasterSubModule']] = relationship('MasterSubModule', back_populates='property_sell_listing')
    user: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[user_id], back_populates='property_sell_listing1')
    property_listing: Mapped[list['PropertyListing']] = relationship('PropertyListing', back_populates='property_sell_listing')


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

    branch: Mapped['InstitutionBranch'] = relationship('InstitutionBranch', back_populates='student_profile')
    student_academic_finance: Mapped['StudentAcademicFinance'] = relationship('StudentAcademicFinance', uselist=False, back_populates='student')
    student_fee_installments: Mapped[list['StudentFeeInstallments']] = relationship('StudentFeeInstallments', back_populates='student')
    student_sem_academic_progress: Mapped[list['StudentSemAcademicProgress']] = relationship('StudentSemAcademicProgress', back_populates='student')


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


class ExamInvigilationAssignment(Base):
    __tablename__ = 'exam_invigilation_assignment'
    __table_args__ = (
        ForeignKeyConstraint(['exam_schedule_id'], ['exam_schedule.id'], name='fk_exam_invigilation_assignment_exam'),
        ForeignKeyConstraint(['staff_id'], ['staff_profile.id'], name='fk_exam_invigilation_assignment_staff'),
        PrimaryKeyConstraint('id', name='pk_exam_invigilation_assignment_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    exam_schedule_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    staff_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    duty_notes: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    exam_schedule: Mapped['ExamSchedule'] = relationship('ExamSchedule', back_populates='exam_invigilation_assignment')
    staff: Mapped['StaffProfile'] = relationship('StaffProfile', back_populates='exam_invigilation_assignment')


class ExamNotificationLog(Base):
    __tablename__ = 'exam_notification_log'
    __table_args__ = (
        ForeignKeyConstraint(['exam_schedule_id'], ['exam_schedule.id'], name='fk_exam_notification_log_exam'),
        PrimaryKeyConstraint('id', name='pk_exam_notification_log_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    exam_schedule_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    message: Mapped[Optional[str]] = mapped_column(String(255))
    sent_count: Mapped[Optional[int]] = mapped_column(Integer)
    failed_count: Mapped[Optional[int]] = mapped_column(Integer)
    retry_success: Mapped[Optional[int]] = mapped_column(Integer)
    scheduled_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    status: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    exam_schedule: Mapped['ExamSchedule'] = relationship('ExamSchedule', back_populates='exam_notification_log')


class ExamReminderSettings(Base):
    __tablename__ = 'exam_reminder_settings'
    __table_args__ = (
        ForeignKeyConstraint(['exam_schedule_id'], ['exam_schedule.id'], name='fk_exam_reminder_settings_exam'),
        PrimaryKeyConstraint('id', name='pk_exam_reminder_settings_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    exam_schedule_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    enable_notifications: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    trigger_time: Mapped[Optional[str]] = mapped_column(String(255))
    notification_sound: Mapped[Optional[str]] = mapped_column(String(150))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    exam_schedule: Mapped['ExamSchedule'] = relationship('ExamSchedule', back_populates='exam_reminder_settings')


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

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='garage')
    sub_service: Mapped['MasterSubService'] = relationship('MasterSubService', back_populates='master_garage')
    master_mechanic: Mapped[list['MasterMechanic']] = relationship('MasterMechanic', back_populates='garage')


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

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='garage_service')
    sub_service: Mapped['MasterSubService'] = relationship('MasterSubService', back_populates='master_garage_service')
    home_service_booking_service_map: Mapped[list['HomeServiceBookingServiceMap']] = relationship('HomeServiceBookingServiceMap', back_populates='garage_service')


class MasterPackageAddOn(Base):
    __tablename__ = 'master_package_add_on'
    __table_args__ = (
        ForeignKeyConstraint(['sub_service_id'], ['master_sub_service.id'], name='fk_master_add_on_sub_service_id'),
        PrimaryKeyConstraint('id', name='pk_master_add_on_id'),
        UniqueConstraint('packages_add_on', name='uk_master_add_on_add_on'),
        UniqueConstraint('sub_service_id', 'packages_add_on', name='uk_master_add_on_sub_service_id_packages_add_on')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('master_add_on_id_seq'), primary_key=True)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    packages_add_on: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    sub_service_id: Mapped[Optional[int]] = mapped_column(Integer)

    sub_service: Mapped[Optional['MasterSubService']] = relationship('MasterSubService', back_populates='master_package_add_on')
    home_service_booking_add_on: Mapped[list['HomeServiceBookingAddOn']] = relationship('HomeServiceBookingAddOn', back_populates='add_on')


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


class MasterVehicleBrand(Base):
    __tablename__ = 'master_vehicle_brand'
    __table_args__ = (
        ForeignKeyConstraint(['sub_service_id'], ['master_sub_service.id'], name='fk_master_vehicle_brand_sub_service_id'),
        PrimaryKeyConstraint('id', name='pk_master_vehicle_brand_id'),
        UniqueConstraint('brand_name', name='uk_master_vehicle_brand_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sub_service_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='brand')
    sub_service: Mapped['MasterSubService'] = relationship('MasterSubService', back_populates='master_vehicle_brand')
    vehicle_brand_fuel: Mapped[list['VehicleBrandFuel']] = relationship('VehicleBrandFuel', back_populates='brand')


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


class ServiceRequests(Base):
    __tablename__ = 'service_requests'
    __table_args__ = (
        CheckConstraint('doctor_id IS NOT NULL AND lab_id IS NULL AND pharmacy_id IS NULL OR doctor_id IS NULL AND lab_id IS NOT NULL AND pharmacy_id IS NULL OR doctor_id IS NULL AND lab_id IS NULL AND pharmacy_id IS NOT NULL', name='ck_service_requests_one_service_only'),
        CheckConstraint("service_type::text = ANY (ARRAY['DOCTOR'::character varying, 'LAB'::character varying, 'PHARMACY'::character varying]::text[])", name='ck_service_requests_service_type'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profile.id'], name='fk_service_requests_doctor_id'),
        ForeignKeyConstraint(['lab_id'], ['available_labs.id'], name='fk_service_requests_lab_id'),
        ForeignKeyConstraint(['pharmacy_id'], ['available_pharmacies.id'], name='fk_service_requests_pharmacy_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_service_requests_user_id'),
        PrimaryKeyConstraint('id', name='pk_service_requests_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    service_type: Mapped[str] = mapped_column(String(50), nullable=False)
    doctor_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    lab_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    pharmacy_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    upload_prescription: Mapped[Optional[str]] = mapped_column(String(500))
    delivery_address: Mapped[Optional[str]] = mapped_column(String(255))
    special_instructions: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'PENDING'::character varying"))
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))

    doctor: Mapped[Optional['DoctorProfile']] = relationship('DoctorProfile', back_populates='service_requests')
    lab: Mapped[Optional['AvailableLabs']] = relationship('AvailableLabs', back_populates='service_requests')
    pharmacy: Mapped[Optional['AvailablePharmacies']] = relationship('AvailablePharmacies', back_populates='service_requests')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='service_requests')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='service_request')
    payments: Mapped[list['Payments']] = relationship('Payments', back_populates='service_request')


class StudentAcademicFinance(Base):
    __tablename__ = 'student_academic_finance'
    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['student_profile.student_id'], name='fk_student_academic_finance_student_id'),
        PrimaryKeyConstraint('id', name='pk_student_academic_finance_id'),
        UniqueConstraint('student_id', name='uk_student_academic_finance_student_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[str] = mapped_column(String(150), nullable=False)
    father_name: Mapped[str] = mapped_column(String(255), nullable=False)
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
    academic_year: Mapped[Optional[str]] = mapped_column(String(100))

    student: Mapped['StudentProfile'] = relationship('StudentProfile', back_populates='student_fee_installments')


class StudentSemAcademicProgress(Base):
    __tablename__ = 'student_sem_academic_progress'
    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['student_profile.student_id'], name='fk_student_sem_academic_progress_student_id'),
        PrimaryKeyConstraint('id', name='pk_student_sem_academic_progress_id'),
        UniqueConstraint('student_id', 'academic_year', 'semester_no', name='uk_student_sem_academic_progress')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[str] = mapped_column(String(150), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(100), nullable=False)
    semester_no: Mapped[int] = mapped_column(Integer, nullable=False)
    sgpa: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    attendance_percent: Mapped[Optional[int]] = mapped_column(Integer)
    backlogs: Mapped[Optional[int]] = mapped_column(Integer)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    student: Mapped['StudentProfile'] = relationship('StudentProfile', back_populates='student_sem_academic_progress')


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


class Appointments(Base):
    __tablename__ = 'appointments'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['PENDING'::character varying, 'CONFIRMED'::character varying, 'CANCELLED'::character varying]::text[])", name='ck_appointments_status'),
        ForeignKeyConstraint(['ambulance_id'], ['master_ambulance.id'], name='fk_appointments_ambulance_id'),
        ForeignKeyConstraint(['assistants_id'], ['master_assistants.id'], name='fk_appointments_assistants_id'),
        ForeignKeyConstraint(['consultation_type_id'], ['master_consultation_type.id'], name='fk_appointments_consultation_type_id'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profile.id'], name='fk_appointments_doctor_id'),
        ForeignKeyConstraint(['doctor_specialization_id'], ['master_doctor_specialization.id'], name='fk_appointments_doctor_specialization_id'),
        ForeignKeyConstraint(['hospital_id'], ['master_hospital.id'], name='appointments_hospital_id_fkey'),
        ForeignKeyConstraint(['labs_id'], ['available_labs.id'], name='fk_appointments_labs_id'),
        ForeignKeyConstraint(['pharmacies_id'], ['available_pharmacies.id'], name='fk_appointments_pharmacies_id'),
        ForeignKeyConstraint(['service_request_id'], ['service_requests.id'], name='appointments_service_request_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_appointments_user_id'),
        PrimaryKeyConstraint('id', name='pk_appointments_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    appointment_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    doctor_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    doctor_specialization_id: Mapped[Optional[int]] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(String)
    days_of_suffering: Mapped[Optional[int]] = mapped_column(Integer)
    health_insurance: Mapped[Optional[bool]] = mapped_column(Boolean)
    required_ambulance: Mapped[Optional[bool]] = mapped_column(Boolean)
    required_assistant: Mapped[Optional[bool]] = mapped_column(Boolean)
    ambulance_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    pickup_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    pharmacies_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    labs_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    consultation_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_request_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    hospital_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'PENDING'::character varying"))
    call_booking_status: Mapped[Optional[str]] = mapped_column(String(255))
    assistants_id: Mapped[Optional[int]] = mapped_column(Integer)

    ambulance: Mapped[Optional['MasterAmbulance']] = relationship('MasterAmbulance', back_populates='appointments')
    assistants: Mapped[Optional['MasterAssistants']] = relationship('MasterAssistants', back_populates='appointments')
    consultation_type: Mapped[Optional['MasterConsultationType']] = relationship('MasterConsultationType', back_populates='appointments')
    doctor: Mapped[Optional['DoctorProfile']] = relationship('DoctorProfile', back_populates='appointments')
    doctor_specialization: Mapped[Optional['MasterDoctorSpecialization']] = relationship('MasterDoctorSpecialization', back_populates='appointments')
    hospital: Mapped[Optional['MasterHospital']] = relationship('MasterHospital', back_populates='appointments')
    labs: Mapped[Optional['AvailableLabs']] = relationship('AvailableLabs', back_populates='appointments')
    pharmacies: Mapped[Optional['AvailablePharmacies']] = relationship('AvailablePharmacies', back_populates='appointments')
    service_request: Mapped[Optional['ServiceRequests']] = relationship('ServiceRequests', back_populates='appointments')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='appointments')
    ambulance_booking: Mapped[list['AmbulanceBooking']] = relationship('AmbulanceBooking', back_populates='appointment')
    payments: Mapped[list['Payments']] = relationship('Payments', back_populates='appointment')


class HomeServiceBookingAddOn(Base):
    __tablename__ = 'home_service_booking_add_on'
    __table_args__ = (
        ForeignKeyConstraint(['add_on_id'], ['master_package_add_on.id'], name='fk_booking_add_on_id'),
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_booking_add_on_created_by'),
        ForeignKeyConstraint(['duration_id'], ['master_duration.id'], name='fk_booking_add_on_duration_id'),
        ForeignKeyConstraint(['home_service_booking_id'], ['home_service_booking.id'], ondelete='CASCADE', name='fk_booking_add_on_booking_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_booking_add_on_modified_by'),
        PrimaryKeyConstraint('id', name='home_service_booking_add_on_pkey'),
        UniqueConstraint('home_service_booking_id', 'add_on_id', name='uq_booking_add_on_unique_combo')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    home_service_booking_id: Mapped[int] = mapped_column(Integer, nullable=False)
    add_on_id: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    add_on: Mapped['MasterPackageAddOn'] = relationship('MasterPackageAddOn', back_populates='home_service_booking_add_on')
    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='home_service_booking_add_on')
    duration: Mapped[Optional['MasterDuration']] = relationship('MasterDuration', back_populates='home_service_booking_add_on')
    home_service_booking: Mapped['HomeServiceBooking'] = relationship('HomeServiceBooking', back_populates='home_service_booking_add_on')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='home_service_booking_add_on_')


class HomeServiceBookingServiceMap(Base):
    __tablename__ = 'home_service_booking_service_map'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['user_registration.id'], name='fk_booking_service_created_by'),
        ForeignKeyConstraint(['garage_service_id'], ['master_garage_service.id'], name='fk_booking_service_garage_service_id'),
        ForeignKeyConstraint(['home_service_booking_id'], ['home_service_booking.id'], ondelete='CASCADE', name='fk_booking_service_booking_id'),
        ForeignKeyConstraint(['modified_by'], ['user_registration.id'], name='fk_booking_service_modified_by'),
        PrimaryKeyConstraint('id', name='home_service_booking_service_map_pkey'),
        UniqueConstraint('home_service_booking_id', 'garage_service_id', name='uq_booking_service')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    home_service_booking_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    garage_service_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    quantity: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))
    service_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user_registration: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[created_by], back_populates='home_service_booking_service_map')
    garage_service: Mapped['MasterGarageService'] = relationship('MasterGarageService', back_populates='home_service_booking_service_map')
    home_service_booking: Mapped['HomeServiceBooking'] = relationship('HomeServiceBooking', back_populates='home_service_booking_service_map')
    user_registration_: Mapped[Optional['UserRegistration']] = relationship('UserRegistration', foreign_keys=[modified_by], back_populates='home_service_booking_service_map_')


class MasterMechanic(Base):
    __tablename__ = 'master_mechanic'
    __table_args__ = (
        ForeignKeyConstraint(['garage_id'], ['master_garage.id'], name='fk_master_mechanic_garage_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_master_mechanic_user_id'),
        PrimaryKeyConstraint('id', name='pk_master_mechanic_id'),
        UniqueConstraint('garage_id', 'user_id', name='uk_mechanic_garage_garage_id_user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    garage_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    rating: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    mechanic_name: Mapped[Optional[str]] = mapped_column(String(255))

    home_service_booking: Mapped[list['HomeServiceBooking']] = relationship('HomeServiceBooking', back_populates='mechanic')
    garage: Mapped['MasterGarage'] = relationship('MasterGarage', back_populates='master_mechanic')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='master_mechanic')


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


class Payments(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        CheckConstraint("payment_method::text = ANY (ARRAY['CARD'::character varying, 'UPI'::character varying, 'CASH'::character varying]::text[])", name='ck_payments_method'),
        CheckConstraint("payment_status::text = ANY (ARRAY['PENDING'::character varying, 'CONFIRMED'::character varying, 'FAILED'::character varying, 'SUCCESS'::character varying]::text[])", name='ck_payments_status'),
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], name='fk_payments_appointment_id'),
        ForeignKeyConstraint(['service_request_id'], ['service_requests.id'], name='fk_payments_service_request_id'),
        ForeignKeyConstraint(['user_id'], ['user_registration.id'], name='fk_payments_user_id'),
        PrimaryKeyConstraint('id', name='pk_payments_id'),
        UniqueConstraint('transaction_id', name='uk_payments_transaction')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    service_request_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    appointment_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    payment_status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'PENDING'::character varying"))
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100))
    remarks: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    modified_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    modified_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='payments')
    service_request: Mapped['ServiceRequests'] = relationship('ServiceRequests', back_populates='payments')
    user: Mapped['UserRegistration'] = relationship('UserRegistration', back_populates='payments')
