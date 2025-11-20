from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import hashlib

app = FastAPI()

users_db = {}

class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    mobile_number: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    full_name: str
    email: EmailStr
    mobile_number: str
    password_hash: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# Helper function for consistent API response
def api_response(success: bool, message: str, data=None, error=None, status_code=200):
    return {
        "success": success,
        "message": message,
        "data": data,
        "error": error,
        "status_code": status_code
    }


@app.post("/signup")
def signup(request: SignupRequest):
    if request.email in users_db:
        raise HTTPException(
            status_code=400,
            detail=api_response(False, "Email already registered", None, "Duplicate email", 400)
        )

    password_hash = hash_password(request.password)
    user = User(
        full_name=request.full_name,
        email=request.email,
        mobile_number=request.mobile_number,
        password_hash=password_hash
    )

    users_db[request.email] = user

    # Example: you can generate ids dynamically later
    return api_response(
        success=True,
        message="User created successfully",
        data={
            "user_id": len(users_db),  
        },
        error=None,
        status_code=200
    )


@app.post("/login")
def login(request: LoginRequest):
    user = users_db.get(request.email)

    if not user or user.password_hash != hash_password(request.password):
        raise HTTPException(
            status_code=401,
            detail=api_response(False, "Invalid email or password", None, "Auth failed", 401)
        )

    return api_response(
        success=True,
        message="Login successful",
        data={
            "user_id": list(users_db.keys()).index(request.email) + 1
        },
        error=None,
        status_code=200
    )
