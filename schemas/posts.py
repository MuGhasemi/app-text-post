from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class UserDisplay(BaseModel):
    """
    Schema returned when a post is retrieved.

    Attributes:
        username (str): Username of the User.
    """
    username: str

    model_config = ConfigDict(from_attributes=True)


class CreatePost(BaseModel):
    """
    Schema for creating a new post.

    Attributes:
        title (str): Title of the post.
        description (str): Content or description of the post.
    """
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class ResponsePost(BaseModel):
    """
    Schema returned when a post is retrieved.

    Attributes:
        id (UUID): Unique post identifier.
        title (str): Title of the post.
        description (str): Post content.
        owner (UserDisplay): User of the post owner.
        created_at (datetime): Post creation timestamp.
        updated_at (datetime): Last update timestamp.
    """
    id: UUID
    title: str
    description: str
    owner: UserDisplay
    number_of_post_likes: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdatePost(BaseModel):
    """
    Schema for updating a post.

    All fields are optional. Only provided fields
    will be updated.

    Attributes:
        title (str | None): New title.
        description (str | None): New description.
    """
    title: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DeletePost(BaseModel):
    """
    Schema for deleting a post.
    """

    model_config = ConfigDict(from_attributes=True)
