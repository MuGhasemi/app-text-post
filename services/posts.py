from fastapi import HTTPException, status
from schemas.posts import CreatePost, UpdatePost, DeletePost
from sqlalchemy.orm import Session
from models.posts import Post
from models.users import User
from models.likes import Like
from sqlalchemy import func
from services.likes import number_of_post_likes


def format_posts_with_likes(rows) -> list[dict[str, int]]:
    """
    Convert query results into dictionaries for the post response.

    Each row contains a Post object and its like count.
    The function extracts the required post fields and adds
    the number of likes to each dictionary.

    Args:
        rows: Query results containing Post objects and like counts.

    Returns:
        list[dict]: Post data with owner information and like counts.
    """
    return [
        {
            "id": post.id,
            "title": post.title,
            "description": post.description,
            "owner": post.owner,
            "number_of_post_likes": like_count,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }
        for post, like_count in rows
    ]


def explore(db: Session, search: str | None = None) -> list[dict[str, int]]:
    """
    Retrieve public posts with their like counts.

    Optionally filter posts by an exact title match.
    Include posts with zero likes in the results.

    Args:
        search (str | None): Optional exact title filter.
        db (Session): Database session.

    Returns:
        list[dict]: Public posts with owner information and like counts.

    Raises:
        HTTPException:
            404: If no matching posts are found.
    """
    query = (
        db.query(
            Post,
            func.count(Like.id).label("number_of_post_likes"),
        )
        .outerjoin(Like, Like.post_id == Post.id)
    )

    if search is not None:
        query = query.filter(Post.title == search)

    rows = query.group_by(Post.id).all()

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Posts!",
        )

    return format_posts_with_likes(rows)


def get_all_posts_current_user(db: Session, current_user: User) -> list[dict[str, int]]:
    """
    Retrieve posts owned by the authenticated user.

    Include the like count for each post.

    Args:
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        list[dict]: The user's posts with owner information and like counts.

    Raises:
        HTTPException:
            404: If no matching posts are found.
    """
    query = db.query(Post, func.count(Like.id).label("number_of_post_likes"),
                     ).outerjoin(Like, Like.post_id == Post.id).filter(Post.owner_id == current_user.id)
    rows = query.group_by(Post.id).all()
    # if not rows:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Not Posts!",
    #     )
    return format_posts_with_likes(rows)


def get_post_by_title(title: str, db: Session,current_user: User):
    """
    Retrieve a post owned by the authenticated user.

    Search for a post by its exact title and include its like count.

    Args:
        title (str): Exact title of the requested post.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        dict: Post data with owner information and like count.

    Raises:
        HTTPException:
            404: If no matching post is found.
    """
    post: Post = db.query(Post).filter(
        Post.title == title, Post.owner_id == current_user.id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
    return format_posts_with_likes([(post, number_of_post_likes(post.id, db))])[0] # type: ignore


def create_new_post(data: CreatePost, db: Session,current_user: User) -> CreatePost:
    """
    Create a new post for the authenticated user.

    Store the post title, description, and owner ID in the database.

    Args:
        data (CreatePost): Request data containing the post title
            and description.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        CreatePost: The created post data.

    Raises:
        HTTPException:
            400: If the ownership validation fails.
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


def update_post(title: str, data: UpdatePost, db: Session,current_user: User) -> UpdatePost:
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


def delete_post(title: str, db: Session,current_user: User) -> DeletePost:
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
