from fastapi import Depends, HTTPException, status
from schemas.posts import ResponsePost, CreatePost, UpdatePost
from sqlalchemy.orm import Session
from models.posts import Post
from models.users import User
from dependencies import get_db
from core.security import get_current_user


def explore(search: str | None = None, db: Session = Depends(get_db)) -> list[Post] | None:
    """
    Retrieve public posts.

    If a search value is provided, only posts
    matching the title are returned.

    Args:
        search (str | None): Post title filter.
        db (Session): Database session.

    Returns:
        list[Post]: List of matching posts.

    Raises:
        HTTPException:
            If no posts are found.
    """
    if search is not None:
        posts: list[Post] = db.query(Post).filter(Post.title == search).all()
        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not Posts!")
        return posts
    posts: list[Post] = db.query(Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Posts!")
    return posts


def get_all_posts_current_user(search: str | None = None,
                               db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_user)) -> list[Post] | None:
    """
    Retrieve all posts owned by the current user.

    Args:
        search (str | None): Optional title filter.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        list[Post]: User posts.

    Raises:
        HTTPException:
            If no posts are found.
    """
    if search is not None:
        posts: list[Post] = db.query(Post).filter(
            Post.owner_id == current_user.id, Post.title == search).all()
        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not Posts!")
        return posts
    posts: list[Post] = db.query(Post).filter(
        Post.owner_id == current_user.id).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Posts!")
    return posts


def get_post_by_title(title: str, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)) -> ResponsePost:
    """
    Retrieve a single post by title.

    Args:
        title (str): Post title.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ResponsePost: Requested post.

    Raises:
        HTTPException:
            If the post does not exist.
    """
    post: Post = db.query(Post).filter(
        Post.title == title, Post.owner_id == current_user.id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found!")
    return post


def create_new_post(data: CreatePost, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)) -> ResponsePost:
    """
    Create a new post for the authenticated user.

    Args:
        data (CreatePost): Post data.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ResponsePost: Created post.

    Raises:
        HTTPException:
            If the request is invalid.
    """
    db_post: Post = Post(title=data.title,
                         description=data.description,
                         owner_id=current_user.id)
    if current_user.id != db_post.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="bad request!")
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(title: str, data: UpdatePost, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> ResponsePost:
    """
    Update an existing post.

    Args:
        title (str): Post title.
        data (UpdatePost): Updated fields.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ResponsePost: Updated post.

    Raises:
        HTTPException:
            If the post is not found.
    """
    post = db.query(Post).filter(Post.title == title,
                                 Post.owner_id == current_user.id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found!")
    updated_filed = data.model_dump(exclude_unset=True)
    for key, value in updated_filed.items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


def delete_post(title: str, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> ResponsePost:
    """
    Delete a post owned by the authenticated user.

    Args:
        title (str): Post title.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ResponsePost: Deleted post.

    Raises:
        HTTPException:
            If the post does not exist.
    """
    post: Post = db.query(Post).filter(
        Post.title == title, Post.owner_id == current_user.id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found!")
    db.delete(post)
    db.commit()
    return post
