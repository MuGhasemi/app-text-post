from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from datetime import datetime, timezone
import uuid


class Like(Base):
    """
    SQLAlchemy model representing a like on a post.

    Each like belongs to one user and one post.
    The model stores references to the user and post,
    along with the timestamp when the like was created.

    Attributes:
        id (UUID): Unique identifier of the like.
        owner_id (UUID): Foreign key referencing the user who liked the post.
        post_id (UUID): Foreign key referencing the liked post.
        created_at (datetime): Timestamp when the like was created.
        owner (User): Relationship to the user who created the like.
        post (Post): Relationship to the post that received the like.
    """

    __tablename__ = "likes"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )

    owner_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    post_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("posts.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="likes"
    )

    post = relationship(
        "Post",
        back_populates="likes"
    )
