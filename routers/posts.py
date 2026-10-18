from fastapi import APIRouter, Depends, HTTPException, status
from schemas.posts import ResponsePost, CreatePost, UpdatePost, DeletePost
from sqlalchemy.orm import Session
from models.posts import Post
from models.users import User
from dependencies import get_db
from core.security import get_current_user
from services.posts import (explore, get_all_posts_current_user,
                            get_post_by_title, create_new_post, update_post, delete_post)

router: APIRouter = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/explore", status_code=status.HTTP_200_OK, response_model=list[ResponsePost])
def route_of_explore(search: str | None = None, db: Session = Depends(get_db)):
    """
    Handle requests for exploring public posts.

    Args:
        search (str | None): Optional post title to search for.
        db (Session): Database session.

    Returns:
        list[Post]: List of public posts.
    """
    return explore(db, search)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ResponsePost])
def route_of_get_all_posts_current_user(db: Session = Depends(get_db),
                                        current_user: User = Depends(get_current_user)):
    """
    Handle requests for retrieving the current user's posts.

    Args:
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        list[Post]: Posts owned by the current user.
    """
    return get_all_posts_current_user(db, current_user)


@router.get("/{title}", status_code=status.HTTP_200_OK, response_model=ResponsePost)
def route_of_get_post_by_title(title: str, db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_user)):
    """
    Handle requests for retrieving a post by title.

    Args:
        title (str): Title of the requested post.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ResponsePost: Requested post.
    """
    return get_post_by_title(title, db, current_user)


@router.post("/new", response_model=CreatePost, status_code=status.HTTP_201_CREATED)
def route_of_create_new_post(data: CreatePost, db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_user)):
    """
    Handle requests for creating a new post.

    Args:
        data (CreatePost): New post data.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ResponsePost: Newly created post.
    """
    return create_new_post(data, db, current_user)


@router.put("/{title}", response_model=UpdatePost, status_code=status.HTTP_200_OK)
def route_of_update_post(title: str, data: UpdatePost, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    """
    Handle requests for updating an existing post.

    Args:
        title (str): Title of the post to update.
        data (UpdatePost): Updated post data.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ResponsePost: Updated post.
    """
    return update_post(title, data, db, current_user)


@router.delete("/{title}", response_model=DeletePost, status_code=status.HTTP_200_OK)
def route_of_delete_post(title: str, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    """
    Handle requests for deleting a post.

    Args:
        title (str): Title of the post to delete.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ResponsePost: Deleted post.
    """
    return delete_post(title, db, current_user)
