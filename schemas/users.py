from pydantic import BaseModel


class CreateUser(BaseModel):
    """
    Schema for user registration.

    Attributes:
        username (str): User username.
        password (str): Plain-text password.
    """
    username: str
    password: str


class UserProfile(BaseModel):
    """
    Schema representing public user profile information.

    Attributes:
        username (str): Username of the user.
    """
    username: str


class UpdateUser(BaseModel):
    """
    Schema for updating user information.

    Attributes:
        username (str): New username.
    """
    username: str


class Token(BaseModel):
    """
    Schema returned after successful authentication.

    Attributes:
        access_token (str): JWT access token.
        token_type (str): Authentication type.
    """
    access_token: str
    token_type: str
