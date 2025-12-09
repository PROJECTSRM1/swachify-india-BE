
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException,Request
from app.config.settings import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_EXPIRE_MINUTES = settings.JWT_EXPIRE_MINUTES
REFRESH_EXPIRE_DAYS = settings.REFRESH_EXPIRE_DAYS


def create_access_token(subject: dict) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=ACCESS_EXPIRE_MINUTES)

    payload = subject.copy()  # include sub, role, email, etc.
    payload.update({
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "access",
    })

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



def create_refresh_token(subject: dict) -> str:
    now = datetime.utcnow()
    expire = now + timedelta(days=REFRESH_EXPIRE_DAYS)

    payload = subject.copy()  # include sub, role, email, etc.
    payload.update({
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "refresh",
    })

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    print("\n========== VERIFY TOKEN CALLED ==========")
    print("TOKEN RECEIVED:", token)
    print("TOKEN LENGTH:", len(token))
    print("USING SECRET_KEY:", SECRET_KEY)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("DECODE SUCCESS PAYLOAD:", payload)
        return payload

    except ExpiredSignatureError as e:
        print("ERROR TYPE: ExpiredSignatureError")
        print("ERROR MESSAGE:", str(e))
        raise HTTPException(status_code=440, detail="Session expired. Please login again.")

    except JWTError as e:
        print("ERROR TYPE:", type(e).__name__)
        print("ERROR MESSAGE:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")



def is_admin_already_logged_in(request: Request):
    token = request.headers.get("Authorization")

    if not token:
        return False

    try:
        token = token.replace("Bearer ", "")
        payload = verify_token(token)

        # If token is valid and role is admin → already logged in
        if payload.get("role") == "admin":
            return True

        return False

    except:
        return False  # token invalid or expired
    
def verify_admin_token(token: str) -> dict:
    payload = verify_token(token)
    
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Admin privileges required."
        )

    return payload
