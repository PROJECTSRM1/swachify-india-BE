from datetime import datetime, timedelta
from jose import jwt
import os

SECRET = os.getenv("JWT_SECRET")
ALGO = os.getenv("JWT_ALGORITHM")
ACCESS_EXP_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 2))
REFRESH_EXP_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXP_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET, algorithm=ALGO)


def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_EXP_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET, algorithm=ALGO)


