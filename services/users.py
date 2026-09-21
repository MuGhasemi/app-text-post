from fastapi import Depends, HTTPException, status
from schemas.users import CreateUser, UserProfile, UpdateUser
from sqlalchemy.orm import Session
from models.users import User
from dependencies import get_db
from fastapi.security import OAuth2PasswordRequestForm
from core.security import (verify_password,
                           create_access_token,
                           hash_password,
                           get_user,
                           get_current_user,
                           oauth2_scheme,
                           BLACKLISTED_TOKENS)


def sign_up(data: CreateUser, db: Session = Depends(get_db)) -> UserProfile:
    """
        Register a new user.

        Args:
            data (CreateUser): User registration data.
            db (Session): Database session.

        Returns:
            User: Created user.

        Raises:
            HTTPException:
                If the username already exists.
        """
    db_user: User = get_user(data.username, db)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered!")
    db_user: User = User(username=data.username,
                         hashed_password=hash_password(data.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Authenticate a user and generate an access token.

    Args:
        data (OAuth2PasswordRequestForm):
            User credentials.
        db (Session): Database session.

    Returns:
        Token: JWT token information.

    Raises:
        HTTPException:
            If credentials are invalid.
    """
    user: User = get_user(data.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password!")
    if not verify_password(data.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password!")
    access_token = create_access_token({"sub": str(user.username)})
    return {"access_token": access_token,
            "token_type": "bearer"}


def logout(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    """
    Log out the current user.

    The current token is added to the blacklist.

    Args:
        token (str): JWT token.

    Returns:
        dict: Logout confirmation message.
    """
    BLACKLISTED_TOKENS.add(token)
    return {"message": "Logged out successfully"}


def get_user_detail(db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)) -> UserProfile:
    """
    Retrieve the authenticated user's profile.

    Args:
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        UserProfile: User profile information.

    Raises:
        HTTPException:
            If the user is not found.
    """
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    return db_user


def update_user_detail(data: UpdateUser, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)) -> UserProfile:
    """
    Update user profile information.

    Args:
        data (UpdateUser): Updated user data.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        UserProfile: Updated profile information.
    """
    db_user = db.query(User).filter(User.id == current_user.id).first()
    updated_filed = data.model_dump(exclude_unset=True)
    for key, value in updated_filed.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
