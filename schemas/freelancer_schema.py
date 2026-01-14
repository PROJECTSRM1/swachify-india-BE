# from pydantic import BaseModel, EmailStr, field_validator
# from typing import Optional
# from datetime import date
# import re

# VALID_GOV_ID_TYPES=["aadhar","pan","voter","driving_license"]

# class FreelancerRegister(BaseModel):
#     first_name: str
#     last_name: Optional[str] = None
#     email: EmailStr
#     mobile: str
#     password: str
#     confirm_password: str
#     gender_id: int
#     state_id: Optional[int] = None
#     district_id: Optional[int] = None
#     skill_id: Optional[int] = None
#     government_id_type: Optional[str] = None
#     government_id_number: Optional[str] = None

#     address: Optional[str] = None
#     experience_summary: Optional[str] = None
#     experience_doc: Optional[str] = None  # Assuming this is a URL or file path
   
#     @field_validator("email")
#     def check_gmail(cls, value):
#         if not value.endswith("@gmail.com"):
#             raise ValueError("Email must end with @gmail.com")
#         return value

   
#     @field_validator("mobile")
#     def check_mobile(cls, value):
#         pattern = r"^[6-9]\d{9}$"
#         if not re.fullmatch(pattern, value):
#             raise ValueError("Mobile must be 10 digits starting with 6,7,8,9")
#         return value

    
#     @field_validator("password")
#     def strong_password(cls, value):
   
#      if len(value) > 72:
#         raise ValueError("Password cannot exceed 72 characters (bcrypt limit).")

#      pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"
#      if not re.match(pattern, value):
#         raise ValueError(
#             "Password must contain at least 8 characters including uppercase, lowercase, number, and special character."
#         )
#      return value

   
#     @field_validator("confirm_password")
#     def match_password(cls, value, info):
#         password = info.data.get("password")
#         if password and value != password:
#             raise ValueError("Password and Confirm Password do not match.")
#         return value

#     @field_validator("government_id_type")
#     def validate_gov_type(cls, value):
#         if value and value.lower() not in VALID_GOV_ID_TYPES:
#             raise ValueError(f"government_id_type must be one of {VALID_GOV_ID_TYPES}")
#         return value.lower() if value else value

#     @field_validator("government_id_number")
#     def validate_gov_number(cls, value, info):
#         gov_type = info.data.get("government_id_type")

#         if not value:
#             return value

#         if not gov_type:
#             raise ValueError("government_id_type is required")

#         patterns = {
#             "aadhar": r"^\d{12}$",
#             "pan": r"^[A-Z]{5}\d{4}[A-Z]$",
#             "voter": r"^[A-Z]{3}\d{7}$",
#             "driving_license": r"^[A-Z]{2}\d{2}\s?\d{11}$",
#         }

#         if gov_type in patterns and not re.fullmatch(patterns[gov_type], value):
#             raise ValueError(f"Invalid {gov_type} number format")

#         return value
    



# class FreelancerLogin(BaseModel):
#     email_or_phone: str
#     password: str

#     @field_validator("email_or_phone")
#     def validate_identifier(cls, value):
#         value = value.strip()
#         email_pattern = r"^\S+@\S+\.\S+$"
#         mobile_pattern = r"^[6-9]\d{9}$"
#         if not (re.match(email_pattern, value) or re.match(mobile_pattern, value)):
#             raise ValueError("Enter valid email or 10-digit mobile number")
#         return value
    
#     @field_validator("password")
#     def validate_password(cls, value):
#         value = value.strip()
#         if len(value) < 6:
#             raise ValueError("Password must be at least 6 characters.")
#         if len(value) > 72:
#             raise ValueError("Password cannot exceed bcrypt limit (72 characters).")
#         return value
    
# class FreelancerLogout(BaseModel):
#     user_id: int


from pydantic import BaseModel, field_validator
import re

# ==================================================
# 🔹 FREELANCER LOGIN
# ==================================================
class FreelancerLogin(BaseModel):
    """
    Freelancer login request.
    Note: Freelancer registration is handled by unified /api/auth/register endpoint with work_type=2
    """
    email_or_phone: str
    password: str
    
    @field_validator("email_or_phone")
    @classmethod
    def validate_identifier(cls, v):
        v = v.strip()
        email_pattern = r"^\S+@\S+\.\S+$"
        mobile_pattern = r"^[6-9]\d{9}$"
        if not (re.match(email_pattern, v) or re.match(mobile_pattern, v)):
            raise ValueError("Enter valid email or 10-digit mobile number")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        v = v.strip()
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        if len(v) > 72:
            raise ValueError("Password cannot exceed 72 characters (bcrypt limit)")
        return v

