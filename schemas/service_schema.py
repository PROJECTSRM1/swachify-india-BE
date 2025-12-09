# from pydantic import BaseModel, EmailStr, Field, validator
# from typing import List, Optional
# import re
# from datetime import date


# class ServiceOrder(BaseModel):

#     mainCategoryKey: str = Field(..., min_length=2)
#     subCategoryKey: str = Field(..., min_length=2)

#     moduleTitle: str = Field(..., min_length=3)
#     moduleDescription: str = Field(..., min_length=5)

#     basePrice: float = Field(..., gt=0)

#     serviceType: str = Field(..., min_length=2)

#     propertySizeSqft: Optional[int] = Field(default=None, ge=0)
#     bedrooms: Optional[int] = Field(default=None, ge=0)
#     bathrooms: Optional[int] = Field(default=None, ge=0)

#     preferredDate: date

#     addons: List[str] = Field(default_factory=list)

#     instructions: Optional[str] = Field(default=None, max_length=500)

#     fullName: str = Field(..., min_length=3)
#     email: EmailStr
#     mobile: str = Field(..., min_length=10, max_length=10)
#     address: str = Field(..., min_length=5)

#     computedPrice: float = Field(..., gt=0)

#     @validator("mobile")
#     def validate_mobile(cls, v):
#         if not re.fullmatch(r"[6-9]\d{9}", v):
#             raise ValueError("Invalid mobile number. Must be 10 digits starting with 6–9")
#         return v

#     @validator("preferredDate")
#     def validate_date(cls, v):
#         if v < date.today():
#             raise ValueError("Preferred date cannot be in the past")
#         return v



# schemas/service_schema.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import date
import re

class ServiceOrder(BaseModel):

    mainCategoryKey: str = Field(..., min_length=2)
    subCategoryKey: str = Field(..., min_length=2)

    moduleTitle: str = Field(..., min_length=3)
    moduleDescription: str = Field(..., min_length=5)

    basePrice: float = Field(..., gt=0)
    serviceType: str = Field(..., min_length=2)

    propertySizeSqft: Optional[int] = Field(default=None, ge=0)
    bedrooms: Optional[int] = Field(default=None, ge=0)
    bathrooms: Optional[int] = Field(default=None, ge=0)

    preferredDate: date

    addons: List[str] = Field(default_factory=list)
    instructions: Optional[str] = Field(default=None, max_length=500)

    fullName: str = Field(..., min_length=3)
    email: EmailStr
    mobile: str = Field(..., min_length=10, max_length=10)
    address: str = Field(..., min_length=5)

    computedPrice: float = Field(..., gt=0)

    @validator("mobile")
    def validate_mobile(cls, v):
        if not re.fullmatch(r"[6-9]\d{9}", v):
            raise ValueError("Invalid mobile number. Must be 10 digits starting with 6–9")
        return v

    @validator("preferredDate")
    def validate_date(cls, v):
        if v < date.today():
            raise ValueError("Preferred date cannot be in the past")
        return v
