from fastapi import APIRouter, Depends, HTTPException
from schemas import Responce_Post, Create_Post
from sqlalchemy.orm import Session
from db import get_db, Post

router: APIRouter = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    posts: list[Post] = db.query(Post).all()
    if posts is None:
        raise HTTPException(status_code=404, detail="Not Posts!")
    return posts


@router.get("/{title}")
def get_post_by_title(title: str, db: Session = Depends(get_db)) -> Responce_Post:
    post: Post = db.query(Post).filter(Post.title == title).first()
    if post is None:
        raise HTTPException(status_code=404, detail="post not found!")
    return post


@router.post("/new", response_model=Responce_Post)
def create_new_post(data: Create_Post, db: Session = Depends(get_db)) -> Responce_Post:
    db_post: Post = Post(**data.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# not complete
@router.put("/{title}")
def update_post(title: str):
    pass


@router.delete("/{title}", response_model=Responce_Post)
def delete_post(title: str, db: Session = Depends(get_db)) -> Responce_Post:
    post: Post = db.query(Post).filter(Post.title == title).first()
    db.delete(post)
    db.commit()
    return post
