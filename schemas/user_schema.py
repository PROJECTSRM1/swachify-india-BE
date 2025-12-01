from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    confirm_password: str
    gender_id: int 

class LoginRequest(BaseModel):
    email_or_phone: str
    password: str

class LoginResponse(BaseModel):
    email_or_phone: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_expires_in: int


class UpdateUser(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    gender_id: int | None = None
    password: str | None = None 


class VerifyTokenRequest(BaseModel):
    token: str

class VerifyTokenResponse(BaseModel):
    authenticated: bool
    token_type: str | None = None
    user_id: int | None = None
    email: str | None = None
    message: str
