from pydantic import BaseModel, ConfigDict
from schemas.posts import ResponsePost


class UserProfile(BaseModel):
    """
    Schema representing public user profile information.

    Attributes:
        username (str): Username of the user.
    """
    username: str

    model_config = ConfigDict(from_attributes=True)


class CreateUser(UserProfile):
    """
    Schema for user registration.

    Attributes:
        password (str): Plain-text password.
    """
    password: str


class UpdateUser(BaseModel):
    """
    Schema for updating user information.

    Attributes:
        username (str): New username.
    """
    username: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """
    Schema returned after successful authentication.

    Attributes:
        access_token (str): JWT access token.
        token_type (str): Authentication type.
    """
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)


class UserHomePage(BaseModel):
    """
    Schema for the authenticated user's home page response.

    Attributes:
        profile (UserProfile): The current user's profile information.
        posts (list[ResponsePost]): A list of posts created by the current user.
    """
    profile: UserProfile
    posts: list[ResponsePost]

    model_config = ConfigDict(from_attributes=True)
