from fastapi import APIRouter, Depends, HTTPException
from schemas import (ResponcePost, CreatePost, UpdatePost,
                     CreateUser, Token)
from sqlalchemy.orm import Session
from db import get_db, Post, User
from security import verify_password, create_access_token, hash_password

post_router: APIRouter = APIRouter(prefix="/posts", tags=["posts"])
user_router: APIRouter = APIRouter(prefix="/user", tags=["users"])


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


def get_user(username: str, db: Session = Depends(get_db)) -> User:
    return db.query(User).filter(User.username == username).first()


@user_router.post("/sign_up")
def signup(data: CreateUser, db: Session = Depends(get_db)):
    db_user: User = get_user(data.username, db)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    db_user: User = User(username=data.username,
                         hashed_password=hash_password(data.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.get("/login", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    user: User = get_user(username, db)
    if user is None:
        raise HTTPException(
            status_code=401, detail="invalid username or password")
    if not verify_password(password, str(user.hashed_password)):
        raise HTTPException(
            status_code=401, detail="invalid username or password")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token,
            "token_type": "bearer", }
