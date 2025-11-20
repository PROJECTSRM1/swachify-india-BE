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

@app.post("/signup")
def signup(request: SignupRequest):
    if request.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    password_hash = hash_password(request.password)
    user = User(
        full_name=request.full_name,
        email=request.email,
        mobile_number=request.mobile_number,
        password_hash=password_hash
    )
    users_db[request.email] = user
    return {"message": "Signup successful"}

@app.post("/login")
def login(request: LoginRequest):
    user = users_db.get(request.email)
    if not user or user.password_hash != hash_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful"}
