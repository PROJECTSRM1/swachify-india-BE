from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import Dict

from sqlalchemy.orm import Session

from models.user_registration import UserRegistration
from utils.hash_utils import hash_password
from utils.otp_utils import generate_otp
from utils.mail_agent import send_forgot_password_otp
from utils.jwt_utils import create_reset_token, verify_token

OTP_EXP_MINUTES = 10
RESET_TOKEN_EXP_MINUTES = 15


class UserNotFound(Exception):
    pass


class InvalidOtp(Exception):
    pass


class OtpExpired(Exception):
    pass


@dataclass
class OtpEntry:
    user_id: int
    expires_at: datetime
    used: bool = False

otp_store: Dict[str, OtpEntry] = {}


async def request_password_reset(email: str, db: Session) -> None:
    """
    STEP 1: user submits email.
    Check user exists, generate OTP, store in memory, send email with first name.
    """
    user = db.query(UserRegistration).filter(UserRegistration.email == email).first()
    if not user:
        raise UserNotFound("Email not registered")
    otp = generate_otp()
    while otp in otp_store:
        otp = generate_otp()

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=OTP_EXP_MINUTES)

    otp_store[otp] = OtpEntry(
        user_id=user.id,
        expires_at=expires_at,
        used=False,
    )

    first_name = getattr(user, "first_name", None) or "User"

    try:
        await send_forgot_password_otp(user.email, otp, first_name)
    except Exception as e:
        print("ERROR SENDING RESET OTP EMAIL:", repr(e))


def verify_otp(otp: str, db: Session) -> str:
    """
    STEP 2: user submits OTP ONCE (no email).
    - Validate OTP
    - Mark it as used
    - Create & return a short-lived reset token (JWT)
    """
    entry = otp_store.get(otp)
    if not entry:
        raise InvalidOtp("Invalid OTP")

    if entry.used:
        raise InvalidOtp("OTP already used")

    now = datetime.now(timezone.utc)
    if entry.expires_at < now:
        raise OtpExpired("OTP expired")

    entry.used = True

    user = db.query(UserRegistration).filter(UserRegistration.id == entry.user_id).first()
    if not user:
        raise UserNotFound("User not found")

    reset_token = create_reset_token(
        {"user_id": user.id, "email": user.email},
        expires_minutes=RESET_TOKEN_EXP_MINUTES,
    )
    return reset_token


def reset_password(reset_token: str, new_password: str, db: Session) -> None:
    """
    STEP 3: user submits ONLY new password.
    We read reset_token from cookie, verify it, and update password.
    """
    payload = verify_token(reset_token)

    if payload.get("type") != "reset":
        raise InvalidOtp("Invalid reset token")

    user_id = int(payload["sub"])

    user = db.query(UserRegistration).filter(UserRegistration.id == user_id).first()
    if not user:
        raise UserNotFound("User not found")

    user.password = hash_password(new_password)
    db.commit()
