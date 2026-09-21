from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from db.database import Base
import uuid


class Post(Base):
    """
    SQLAlchemy model representing a post.

    A post belongs to one user and contains its title,
    description, and creation and update timestamps.

    Attributes:
        id (UUID): Unique identifier of the post.
        title (str): Title of the post.
        description (str): Content or description of the post.
        created_at (datetime): Post creation timestamp.
        updated_at (datetime): Last update timestamp.
        owner_id (UUID): ID of the user who owns the post.
        owner (User): User who owns the post.
    """

    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )

    title = Column(String)
    description = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    owner_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="items"
    )
