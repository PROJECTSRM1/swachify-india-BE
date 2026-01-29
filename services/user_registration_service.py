# import uuid
# from datetime import date
# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status

# from models.user_registration import UserRegistration
# from models.master_module import MasterModule
# from models.user_services import UserServices
# from models.user_skill import UserSkill
# from schemas.user_schema import RegisterUser
# from utils.hash_utils import hash_password
# from core.constants import (
#     CUSTOMER_ROLE_ID,
#     FREELANCER_ROLE_ID,
#     STATUS_ACTIVE,
#     STATUS_PENDING
# )


# def calculate_age(dob: date | None) -> int | None:
#     if not dob:
#         return None
#     today = date.today()
#     return today.year - dob.year - (
#         (today.month, today.day) < (dob.month, dob.day)
#     )


# def get_message(work_type: int) -> str:
#     if work_type == 1:
#         return "Customer registered successfully"
#     if work_type == 2:
#         return "Freelancer registered successfully. Awaiting admin approval"
#     return "Registered as Customer & Freelancer. Awaiting approval"

# def register_user(db: Session, payload: RegisterUser):

#     # 🔹 Validate services from master_module
#     modules = (
#         db.query(MasterModule)
#         .filter(
#             MasterModule.id.in_(payload.service_ids),
#             MasterModule.is_active == True
#         )
#         .all()
#     )

#     if len(modules) != len(payload.service_ids):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid service IDs"
#         )

#     # 🔹 Duplicate checks
#     if db.query(UserRegistration).filter_by(email=payload.email).first():
#         raise HTTPException(status_code=409, detail="Email already registered")

#     if db.query(UserRegistration).filter_by(mobile=payload.mobile).first():
#         raise HTTPException(status_code=409, detail="Mobile already registered")

#     # 🔹 Role & status
#     if payload.work_type == 1:
#         role_id, status_id = CUSTOMER_ROLE_ID, STATUS_ACTIVE
#     else:
#         role_id, status_id = FREELANCER_ROLE_ID, STATUS_PENDING

#     # 🔹 Create user
#     user = UserRegistration(
#         unique_id=str(uuid.uuid4()),
#         first_name=payload.first_name,
#         last_name=payload.last_name,
#         email=payload.email,
#         mobile=payload.mobile,
#         password=hash_password(payload.password),
#         gender_id=payload.gender_id,
#         dob=payload.dob,
#         age=calculate_age(payload.dob),
#         role_id=role_id,
#         status_id=status_id,
#         state_id=payload.state_id,
#         district_id=payload.district_id,
#         address=payload.address,
#         is_active=True
#     )

#     if payload.government_id:
#         user.government_id = [g.model_dump() for g in payload.government_id]

#     if payload.professional_details:
#         pd = payload.professional_details
#         if pd.experience_years is not None:
#             user.experience_in_years = str(pd.experience_years)

#     db.add(user)
#     db.flush()  # ✅ user.id available

#     # ===============================
#     # 🔹 INSERT USER SERVICES
#     # ===============================
#     user_service_ids: list[int] = []

#     for module in modules:
#         us = UserServices(
#             user_id=user.id,
#             module_id=module.id
#         )
#         db.add(us)
#         db.flush()  # ✅ us.id available
#         user_service_ids.append(us.id)

#     # ===============================
#     # 🔹 INSERT USER SKILLS
#     # ===============================
#     user_skill_ids: list[int] = []

#     if payload.professional_details and payload.professional_details.expertise_in:
#         for skill_id in payload.professional_details.expertise_in:
#             sk = UserSkill(
#                 user_id=user.id,
#                 skill_id=skill_id
#             )
#             db.add(sk)
#             db.flush()  # ✅ sk.id available
#             user_skill_ids.append(sk.id)

#     # ===============================
#     # 🔹 STORE PRIMARY IDS IN REGISTRATION
#     # ===============================
#     user.user_services_id = user_service_ids[0] if user_service_ids else None
#     user.user_skill_id = user_skill_ids[0] if user_skill_ids else None

#     db.commit()
#     db.refresh(user)

#     return user, get_message(payload.work_type)



# import uuid
# from datetime import date
# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status

# from models.user_registration import UserRegistration
# from models.master_module import MasterModule
# from models.user_services import UserServices
# from models.user_skill import UserSkill
# from schemas.user_schema import RegisterUser
# from utils.hash_utils import hash_password
# from core.constants import (
#     CUSTOMER_ROLE_ID,
#     FREELANCER_ROLE_ID,
#     STATUS_ACTIVE,
#     STATUS_PENDING
# )


# def calculate_age(dob: date | None) -> int | None:
#     if not dob:
#         return None
#     today = date.today()
#     return today.year - dob.year - (
#         (today.month, today.day) < (dob.month, dob.day)
#     )


# def get_message(work_type: int) -> str:
#     if work_type == 1:
#         return "Customer registered successfully"
#     if work_type == 2:
#         return "Freelancer registered successfully. Awaiting admin approval"
#     return "Registered as Customer & Freelancer. Awaiting approval"

# def register_user(db: Session, payload: RegisterUser):

#     # 🔹 Validate services from master_module
#     modules = (
#         db.query(MasterModule)
#         .filter(
#             MasterModule.id.in_(payload.service_ids),
#             MasterModule.is_active == True
#         )
#         .all()
#     )

#     if len(modules) != len(payload.service_ids):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid service IDs"
#         )

#     # 🔹 Duplicate checks
#     if db.query(UserRegistration).filter_by(email=payload.email).first():
#         raise HTTPException(status_code=409, detail="Email already registered")

#     if db.query(UserRegistration).filter_by(mobile=payload.mobile).first():
#         raise HTTPException(status_code=409, detail="Mobile already registered")

#     # 🔹 Role & status
#     if payload.work_type == 1:
#         role_id, status_id = CUSTOMER_ROLE_ID, STATUS_ACTIVE
#     else:
#         role_id, status_id = FREELANCER_ROLE_ID, STATUS_PENDING

#     # 🔹 Create user
#     user = UserRegistration(
#         unique_id=str(uuid.uuid4()),
#         first_name=payload.first_name,
#         last_name=payload.last_name,
#         email=payload.email,
#         mobile=payload.mobile,
#         password=hash_password(payload.password),
#         gender_id=payload.gender_id,
#         dob=payload.dob,
#         age=calculate_age(payload.dob),
#         role_id=role_id,
#         status_id=status_id,
#         state_id=payload.state_id,
#         district_id=payload.district_id,
#         address=payload.address,
#         is_active=True
#     )

#     if payload.government_id:
#         user.government_id = [g.model_dump() for g in payload.government_id]

#     if payload.professional_details:
#         pd = payload.professional_details
#         if pd.experience_years is not None:
#             user.experience_in_years = str(pd.experience_years)

#     db.add(user)
#     db.flush()  # ✅ user.id available

#     # ===============================
#     # 🔹 INSERT USER SERVICES
#     # ===============================
#     user_service_ids: list[int] = []

#     for module in modules:
#         us = UserServices(
#             user_id=user.id,
#             module_id=module.id
#         )
#         db.add(us)
#         db.flush()  # ✅ us.id available
#         user_service_ids.append(us.id)

#     # ===============================
#     # 🔹 INSERT USER SKILLS
#     # ===============================
#     user_skill_ids: list[int] = []

#     if payload.professional_details and payload.professional_details.expertise_in:
#         for skill_id in payload.professional_details.expertise_in:
#             sk = UserSkill(
#                 user_id=user.id,
#                 skill_id=skill_id
#             )
#             db.add(sk)
#             db.flush()  # ✅ sk.id available
#             user_skill_ids.append(sk.id)

#     # ===============================
#     # 🔹 STORE PRIMARY IDS IN REGISTRATION
#     # ===============================
#     user.user_services_id = user_service_ids[0] if user_service_ids else None
#     user.user_skill_id = user_skill_ids[0] if user_skill_ids else None

#     db.commit()
#     db.refresh(user)

#     return user, get_message(payload.work_type)


# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status

# from models.user_registration import UserRegistration
# from schemas.user_schema import LoginRequest, LoginResponse
# from utils.hash_utils import verify_password
# from utils.jwt_utils import create_access_token, create_refresh_token


# def login_user(db: Session, payload: LoginRequest) -> LoginResponse:

#     user = (
#         db.query(UserRegistration)
#         .filter(
#             (UserRegistration.email == payload.email_or_phone) |
#             (UserRegistration.mobile == payload.email_or_phone)
#         )
#         .first()
#     )

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email/mobile or password"
#         )

#     if not verify_password(payload.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email/mobile or password"
#         )

#     token_payload = {
#         "user_id": user.id,
#         "email": user.email,
#         "role_id": user.role_id
#     }

#     return LoginResponse(
#         user_id=user.id,
#         email_or_phone=payload.email_or_phone,
#         access_token=create_access_token(token_payload),
#         refresh_token=create_refresh_token(token_payload),
#         expires_in=60 * 60,              # 1 hour
#         refresh_expires_in=60 * 60 * 24  # 1 day
#     )




import uuid
from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.generated_models import UserRegistration
from models.generated_models import MasterModule
from models.generated_models import UserServices
from models.generated_models import UserSkill

from schemas.user_schema import (
    RegisterUser,
    LoginRequest,
    LoginResponse
)

from utils.hash_utils import hash_password, verify_password
from utils.jwt_utils import create_access_token, create_refresh_token

from core.constants import (
    CUSTOMER_ROLE_ID,
    FREELANCER_ROLE_ID,
    STUDENT_ROLE_ID,
    STATUS_APPROVED,
    STATUS_PENDING
)

# ==================================================
# 🔹 HELPERS
# ==================================================
def calculate_age(dob: date | None) -> int | None:
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - (
        (today.month, today.day) < (dob.month, dob.day)
    )


def get_message(work_type: int) -> str:
    """
    Generate role-based registration message based on work_type.
    
    Args:
        work_type: 1=Customer, 2=Freelancer, 3=Both
    
    Returns:
        Registration success message indicating user type
    """
    if work_type == 1:
        return "Customer registered successfully"
    if work_type == 2:
        return "Freelancer registered successfully. Awaiting admin approval"
    if work_type == 3:
        return "Registered as Customer & Freelancer. Awaiting approval"
    if work_type == 4:
         return "Student Registered Successfully"
    
def register_user(db: Session, payload: RegisterUser):
    """
    Register a new user with role and status assignment based on work_type.
    
    Work Type Mapping:
        1 = Customer       -> role_id=2, status_id=1 (APPROVED)
        2 = Freelancer     -> role_id=4, status_id=2 (PENDING - needs admin approval)
        3 = Both           -> role_id=4, status_id=2 (PENDING - needs admin approval)
    
    Args:
        db: Database session
        payload: RegisterUser schema containing work_type and user details
    
    Returns:
        Dictionary with user info, tokens, and registration message
    """

    # -------------------------
    # Validate services
    # -------------------------
    modules = (
        db.query(MasterModule)
        .filter(
            MasterModule.id.in_(payload.service_ids),
            MasterModule.is_active.is_(True)
        )
        .all()
    )

    if len(modules) != len(payload.service_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid service IDs"
        )

    # -------------------------
    # Duplicate checks
    # -------------------------
    if db.query(UserRegistration).filter_by(email=payload.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    if db.query(UserRegistration).filter_by(mobile=payload.mobile).first():
        raise HTTPException(status_code=409, detail="Mobile already registered")

    # -------------------------
    # Role & status assignment based on work_type
    # -------------------------
    if payload.work_type == 1:
        # Customer: Immediate approval
        role_id, status_id = CUSTOMER_ROLE_ID, STATUS_APPROVED
    elif payload.work_type == 2:
        # Freelancer or Both: Pending admin approval
        role_id, status_id = FREELANCER_ROLE_ID, STATUS_PENDING
    elif payload.work_type == 3:
        role_id, status_id = FREELANCER_ROLE_ID, STATUS_PENDING
    elif payload.work_type == 4:
        role_id, status_id = STUDENT_ROLE_ID, STATUS_APPROVED  # <-- FIXED assignment
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid work_type. Must be 1 (Customer), 2 (Freelancer), 3 (Both), or 4 (Student)."
        )
        

    # -------------------------
    # Create user
    # -------------------------
    user = UserRegistration(
        unique_id=str(uuid.uuid4()),
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        mobile=payload.mobile,
        password=hash_password(payload.password),
        gender_id=payload.gender_id,
        dob=payload.dob,
        age=calculate_age(payload.dob),
        role_id=role_id,
        status_id=status_id,
        state_id=payload.state_id,
        district_id=payload.district_id,
        address=payload.address,
        is_active=True,
        business_type_id=payload.business_type_id if payload.work_type != 4 else None,
        product_name=payload.product_name if payload.work_type != 4 else None,
        business_description=payload.business_description if payload.work_type != 4 else None,
        org_name=payload.org_name if payload.work_type != 4 else None,
        gst_number=payload.gst_number if payload.work_type != 4 else None,
        job_skill_id=payload.job_skill_id
    )

    if payload.government_id:
        user.government_id = [g.model_dump() for g in payload.government_id]

    if payload.professional_details:
        if payload.professional_details.experience_years is not None:
            user.experience_in_years = str(
                payload.professional_details.experience_years
            )

    db.add(user)
    db.flush()  # user.id available

    service_ids: list[int] = []

    # -------------------------
    # User Services
    # -------------------------
    for module in modules:
        us = UserServices(user_id=user.id, module_id=module.id)
        db.add(us)
        db.flush()  # us.id available
        service_ids.append(us.id)

    skill_ids: list[int] = []
    # -------------------------
    # User Skills
    # -------------------------
    if payload.professional_details:
        for skill_id in payload.professional_details.expertise_in:
            sk = UserSkill(user_id=user.id, skill_id=skill_id)
            db.add(sk)
            db.flush()  # sk.id available
            skill_ids.append(sk.id)

    db.commit()
    db.refresh(user)

    # -------------------------
    # 🔐 CREATE JWT TOKENS
    # -------------------------
    token_payload = {
        "user_id": user.id,
        "status_id": user.status_id,
        "role_id": user.role_id
    }

    access_token = create_access_token(token_payload)
    refresh_token = create_refresh_token(token_payload)

    return {
        "message": get_message(payload.work_type),
        "user_id": user.id,
        "unique_id": user.unique_id,
        "email": user.email,
        "mobile": user.mobile,
        "role_id": user.role_id,
        "status_id": user.status_id,
        "work_type": payload.work_type,
        "service_ids": service_ids,
        "skill_ids": skill_ids,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 60 * 60,
        "refresh_expires_in": 60 * 60 * 24,
        "business_type_id": user.business_type_id,
        "product_name": user.product_name,
        "business_description": user.business_description,
        "org_name": user.org_name,
        "gst_number": user.gst_number,
        "job_skill_id": user.job_skill_id
        # "profile_image": user.profile_image,
        # "experience_summary": user.experience_summary,
        # "experience_doc": user.experience_doc,
        # "reg_payment_done": user.reg_payment_done,
        # "reg_fee": float(user.reg_fee) if user.reg_fee is not None else None,
        # "experience_in_years": user.experience_in_years,
        # "noc_number": user.noc_number,
        # "police_station_name": user.police_station_name,
        # "issue_year": user.issue_year,
        # "upload_noc": user.upload_noc,
        # "latitude": float(user.latitude) if user.latitude is not None else None,
        # "longitude": float(user.longitude) if user.longitude is not None else None
    }


def login_user(db: Session, payload: LoginRequest) -> LoginResponse:

    user = (
        db.query(UserRegistration)
        .filter(
            (UserRegistration.email == payload.email_or_phone) |
            (UserRegistration.mobile == payload.email_or_phone),
            UserRegistration.status_id == STATUS_APPROVED
        )
        .first()
    )

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/mobile or password"
        )

    # ✅ SAVE LATITUDE & LONGITUDE (THIS WAS MISSING)
    if payload.latitude is not None and payload.longitude is not None:
        user.latitude = payload.latitude
        user.longitude = payload.longitude
        db.commit()
        db.refresh(user)

    service_ids = [
        s.module_id
        for s in db.query(UserServices)
        .filter(UserServices.user_id == user.id)
        .all()
    ]

    skill_ids = [
        s.skill_id
        for s in db.query(UserSkill)
        .filter(UserSkill.user_id == user.id)
        .all()
    ]

    role = (
        "customer" if user.role_id == 2
        else "freelancer" if user.role_id == 4
        else "Student" if user.role_id == 5
        else "other"
    )

    role_message = (
        "User logged in as a " f"{role}"
        if role == "Customer" or "Student"
        else "User logged in as a freelancer"
    )

    token_payload = {
        "user_id": user.id,
        "email": user.email,
        "role_id": user.role_id
    }

    return LoginResponse(
        message=role_message,
        user_id=user.id,
        email_or_phone=payload.email_or_phone,
        service_ids=service_ids,
        skill_ids=skill_ids,

        # ✅ NOW THESE WILL NOT BE NULL
        latitude=float(user.latitude) if user.latitude else None,
        longitude=float(user.longitude) if user.longitude else None,

        access_token=create_access_token(token_payload),
        refresh_token=create_refresh_token(token_payload),
        expires_in=3600,
        refresh_expires_in=86400,
        role=role
    )
