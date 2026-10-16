from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from db.database import Base
import uuid


class User(Base):
    """
    SQLAlchemy model representing a user account.

    A user can own multiple posts and create multiple likes.
    The model stores account credentials, account status,
    and creation and update timestamps.

    Attributes:
        id (UUID): Unique identifier of the user.
        username (str): Unique username of the user.
        hashed_password (str): Hashed password used for authentication.
        is_active (bool): Indicates whether the account is active.
        created_at (datetime): Timestamp when the account was created.
        updated_at (datetime): Timestamp when the account was last updated.
        items (list[Post]): Posts owned by the user.
        likes (list[Like]): Likes created by the user.
    """

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

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

    items = relationship(
        "Post",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    likes = relationship(
        "Like",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
