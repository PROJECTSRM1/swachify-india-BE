# utils/hash_utils.py
from passlib.context import CryptContext

# Password hashing context - must match what you use in auth.py (sha256_crypt)
_password_context = CryptContext(
    schemes=["sha256_crypt"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    """
    Hash user passwords using sha256_crypt.
    This must be compatible with login / registration.
    """
    return _password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the stored hash.
    """
    return _password_context.verify(plain_password, hashed_password)

# NOTE: We no longer use bcrypt here.
# OTPs are handled as plain text in memory inside forgot_password_service.py.
# If you ever want separate hashing for non-password text, you can add new
# functions here using hashlib.sha256 etc., without touching bcrypt.
