from fastapi import APIRouter, Depends, HTTPException
from schemas import (ResponcePost, CreatePost, UpdatePost,)
from sqlalchemy.orm import Session
from db import get_db, Post

post_router: APIRouter = APIRouter(prefix="/posts", tags=["posts"])


@post_router.get("/")
def get_posts(db: Session = Depends(get_db)):
    posts: list[Post] = db.query(Post).all()
    if posts is None:
        raise HTTPException(status_code=404, detail="Not Posts!")
    return posts


@post_router.get("/{title}")
def get_post_by_title(title: str, db: Session = Depends(get_db)) -> ResponcePost:
    post: Post = db.query(Post).filter(Post.title == title).first()
    if post is None:
        raise HTTPException(status_code=404, detail="post not found!")
    return post


@post_router.post("/new", response_model=ResponcePost)
def create_new_post(data: CreatePost, db: Session = Depends(get_db)) -> ResponcePost:
    db_post: Post = Post(**data.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@post_router.put("/{title}", response_model=ResponcePost)
def update_post(title: str, data: UpdatePost, db: Session = Depends(get_db)) -> ResponcePost:
    post = db.query(Post).filter(Post.title == title).first()
    if post is None:
        raise HTTPException(status_code=404, detail="post not found!")
    updated_filed = data.model_dump(exclude_unset=True)
    for key, value in updated_filed.items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


@post_router.delete("/{title}", response_model=ResponcePost)
def delete_post(title: str, db: Session = Depends(get_db)) -> ResponcePost:
    post: Post = db.query(Post).filter(Post.title == title).first()
    db.delete(post)
    db.commit()
    return post


