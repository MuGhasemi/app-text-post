from fastapi import APIRouter, Depends, status
from schemas.users import CreateUser, Token, UserProfile, UpdateUser, UserHomePage
from sqlalchemy.orm import Session
from models.users import User
from dependencies import get_db
from fastapi.security import OAuth2PasswordRequestForm
from core.security import oauth2_scheme, get_current_user
from services.users import (sign_up, login, logout,
                            get_user_detail, update_user_detail, user_home_page)

router: APIRouter = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.post("/sign_up", status_code=status.HTTP_201_CREATED, response_model=UserProfile)
def route_of_sign_up(data: CreateUser, db: Session = Depends(get_db)) -> UserProfile:
    """
    Handle user registration requests.

    Args:
        data (CreateUser): New user registration data.
        db (Session): Database session.

    Returns:
        UserProfile: Created user's profile.
    """
    return sign_up(data, db)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def route_of_login(data: OAuth2PasswordRequestForm = Depends(),
                   db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Handle user authentication requests.

    Args:
        data (OAuth2PasswordRequestForm):
            User login credentials.
        db (Session): Database session.

    Returns:
        Token: Authentication token and user ID.

    Raises:
        HTTPException:
            If the username or password is incorrect.
    """
    return login(data, db)


@router.post("/logout", response_model=dict[str, str], status_code=status.HTTP_200_OK)
def route_of_logout(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    """
    Handle user logout requests.

    Args:
        token (str): JWT access token of the authenticated user.

    Returns:
        dict[str, str]: Logout confirmation message.
    """
    return logout(token)


@router.get("/profile", response_model=UserProfile, status_code=status.HTTP_200_OK)
def route_of_get_user_detail(db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_user)) -> UserProfile:
    """
    Handle requests for retrieving the current user's profile.

    Args:
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        UserProfile: Current user's profile.
    """
    return get_user_detail(db, current_user)


@router.put("/profile", response_model=UserProfile, status_code=status.HTTP_200_OK)
def route_of_update_user_detail(data: UpdateUser, db: Session = Depends(get_db),
                                current_user: User = Depends(get_current_user)) -> UserProfile:
    """
    Handle requests for updating the current user's profile.

    Args:
        data (UpdateUser): Updated user information.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        UserProfile: Updated user profile.
    """
    return update_user_detail(data, db, current_user)


@router.get("/home", response_model=UserHomePage,  status_code=status.HTTP_200_OK)
def route_of_user_home_page(db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    """
    Return the authenticated user's home page data.

    This endpoint retrieves the user's profile and posts, then returns
    them in a response that follows the UserHomePage schema.

    Args:
        db (Session): The database session provided by dependency injection.
        current_user (User): The authenticated user provided by the
            authentication dependency.

    Returns:
        UserHomePage: The user's profile and list of posts.

    Raises:
        HTTPException: If authentication fails or a required resource
            cannot be retrieved.
    """
    return user_home_page(db, current_user)
