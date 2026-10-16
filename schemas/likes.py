from pydantic import BaseModel, ConfigDict
from uuid import UUID


class LikePost(BaseModel):
    """
    Schema for a request to like a post.

    Attributes:
        post_id (UUID): Unique identifier of the post to like.
    """
    post_id: UUID

    model_config = ConfigDict(from_attributes=True)


class UnlikePost(LikePost):
    """
    Schema for a request to remove a like from a post.

    Inherits the post ID field and configuration from LikePost.

    Attributes:
        post_id (UUID): Unique identifier of the post to unlike.
    """
