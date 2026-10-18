from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from models.users import User
from dependencies import get_db
from db.database import settings
import jwt


pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
BLACKLISTED_TOKENS = set()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.

    Args:
        password (str): Plain-text password.

    Returns:
        str: Secure hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password (str): User input password.
        hashed_password (str): Stored password hash.

    Returns:
        bool: True if passwords match, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str, db: Session = Depends(get_db)) -> User | None:
    """
    Retrieve a user by username.

    Args:
        username (str): Username to search.
        db (Session): Database session.

    Returns:
        User | None: User object if found, otherwise None.
    """
    return db.query(User).filter(User.username == username).first()


def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """
    Generate a JWT access token.

    Args:
        data (dict): Payload data.
        expires_minutes (int): Token expiration time in minutes.

    Returns:
        str: Encoded JWT token.
    """
    to_encode: dict = data.copy()
    expire: datetime = datetime.now(
        timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User | None:
    """
    Validate JWT token and return authenticated user.

    Args:
        db (Session): Database session.
        token (str): JWT token.

    Returns:
        User: Authenticated user.

    Raises:
        HTTPException:
            If the token is invalid, expired,
            blacklisted, or user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token in BLACKLISTED_TOKENS:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(username, db)
    if user is None:
        raise credentials_exception
    return user
