from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.users import User
from models.likes import Like
from core.security import get_db, get_current_user
from schemas.likes import LikePost, UnlikePost
from uuid import UUID


def like_post(data: LikePost, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)) -> str | None:
    """
    Like a post as the authenticated user.

    Check whether the user has already liked the post.
    If not, create a new like record and save it to the database.

    Args:
        data (LikePost): Request data containing the post ID.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        str | None: A success message if the like is created.

    Raises:
        HTTPException:
            400: If the user has already liked the post.
    """
    db_like: Like = db.query(Like).filter(
        Like.owner_id == current_user.id, Like.post_id == data.post_id).first()
    if db_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You have already liked.")
    db_like: Like = Like(owner_id=current_user.id,
                         post_id=data.post_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return "Like successfully."


def unlike_post(data: UnlikePost, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> str | None:
    """
    Remove the authenticated user's like from a post.

    Find the like record associated with the current user and
    the specified post. Delete the record if it exists.

    Args:
        data (UnlikePost): Request data containing the post ID.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        str | None: A success message if the like is removed.

    Raises:
        HTTPException:
            400: If the user has not liked the post.
    """
    db_unlike: Like = db.query(Like).filter(
        Like.owner_id == current_user.id, Like.post_id == data.post_id).first()
    if db_unlike:
        db.delete(db_unlike)
        db.commit()
        return "Unlike successfully."
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="You have not liked.")


def number_of_post_likes(post_id: UUID, db: Session) -> int:
    """
    Count the likes associated with a post.

    Args:
        post_id (UUID): Request data containing the post ID.
        db (Session): Database session.

    Returns:
        int: Total number of likes for the specified post.
    """
    return db.query(Like).filter(Like.post_id == post_id).count()


def get_current_user_liked_posts(db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user),) -> list[UUID]:
    """
    Retrieve the IDs of posts liked by the authenticated user.

    Args:
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        list[UUID]: IDs of posts liked by the current user.
    """
    liked_post_ids = (
        db.query(Like.post_id)
        .filter(Like.owner_id == current_user.id)
        .all()
    )

    return [post_id for (post_id,) in liked_post_ids]
