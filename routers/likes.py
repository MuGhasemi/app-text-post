from fastapi import APIRouter, Depends, status
from models.users import User
from models.likes import Like
from sqlalchemy.orm import Session
from core.security import get_db, get_current_user
from services.likes import like_post, unlike_post, get_current_user_liked_posts
from schemas.likes import LikePost, UnlikePost
from uuid import UUID


router: APIRouter = APIRouter(
    prefix="/likes",
    tags=["likes"]
)


@router.post("/like", status_code=status.HTTP_200_OK)
def route_of_like_post(data: LikePost, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)) -> str | None:
    """
    Create a like for a post.

    Args:
        data (LikePost): Request data containing the post ID.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        str | None: A message indicating the result.

    Raises:
        HTTPException:
            400: If the user has already liked the post.
    """
    return like_post(data, db, current_user)


@router.post("/unlike", status_code=status.HTTP_200_OK)
def route_of_unlike_post(data: UnlikePost, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)) -> str | None:
    """
    Remove the current user's like from a post.

    Args:
        data (UnlikePost): Request data containing the post ID.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        str | None: A message indicating the result.

    Raises:
        HTTPException:
            400: If the user has not liked the post.
    """
    return unlike_post(data, db, current_user)


@router.get("/mine", response_model=list[UUID])
def route_of_get_my_liked_posts(db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user),) -> list[UUID]:
    """
    Retrieve the IDs of posts liked by the authenticated user.

    Args:
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        list[UUID]: IDs of posts liked by the current user.
    """
    return get_current_user_liked_posts(db, current_user)
