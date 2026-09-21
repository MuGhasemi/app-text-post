from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CreatePost(BaseModel):
    """
    Schema for creating a new post.

    Attributes:
        title (str): Title of the post.
        description (str): Content or description of the post.
    """
    title: str
    description: str


class ResponsePost(BaseModel):
    """
    Schema returned when a post is retrieved.

    Attributes:
        id (UUID): Unique post identifier.
        title (str): Title of the post.
        description (str): Post content.
        owner_id (UUID): ID of the post owner.
        created_at (datetime): Post creation timestamp.
        updated_at (datetime): Last update timestamp.
    """
    id: UUID
    title: str
    description: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime


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
