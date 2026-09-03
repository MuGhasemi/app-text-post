from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt


pwd_context = PasswordHash.recommended()
SECRET_KEY = "J+5Nw+gWUmDUZIbNqDkdKyKqL3A+OWRUCUyl+jH8pGE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode: dict = data.copy()
    expire: datetime = datetime.now(
        timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
