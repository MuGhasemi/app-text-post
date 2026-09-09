from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (ResponcePost, CreatePost, UpdatePost,
                     CreateUser, Token)
from sqlalchemy.orm import Session
from db import get_db, Post, User
from fastapi.security import OAuth2PasswordRequestForm
from security import (verify_password,
                      create_access_token,
                      hash_password,
                      get_user,
                      get_current_user)


post_router: APIRouter = APIRouter(prefix="/posts", tags=["posts"])
user_router: APIRouter = APIRouter(prefix="/user", tags=["users"])


@post_router.get("/explore", status_code=status.HTTP_200_OK)
def explore(db: Session = Depends(get_db)):
    posts: list[Post] = db.query(Post).all()[:10]
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Posts!")
    return posts


@post_router.get("/", status_code=status.HTTP_200_OK)
def get_all_posts_current_user(db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_user)):
    posts: list[Post] = db.query(Post).filter(
        Post.owner_id == current_user.id).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Posts!")
    return posts


@post_router.get("/{title}", status_code=status.HTTP_200_OK)
def get_post_by_title(title: str, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)) -> ResponcePost:
    post: Post = db.query(Post).filter(
        Post.title == title, Post.owner_id == current_user.id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found!")
    return post


@post_router.post("/new", response_model=ResponcePost, status_code=status.HTTP_201_CREATED)
def create_new_post(data: CreatePost, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)) -> ResponcePost:
    db_post: Post = Post(title=data.title,
                         description=data.description,
                         owner_id=current_user.id)
    if current_user.id != db_post.owner_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad request!")
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@post_router.put("/{title}", response_model=ResponcePost, status_code=status.HTTP_200_OK)
def update_post(title: str, data: UpdatePost, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> ResponcePost:
    post = db.query(Post).filter(Post.title == title,
                                 Post.owner_id == current_user.id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found!")
    updated_filed = data.model_dump(exclude_unset=True)
    for key, value in updated_filed.items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


@post_router.delete("/{title}", response_model=ResponcePost, status_code=status.HTTP_200_OK)
def delete_post(title: str, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> ResponcePost:
    post: Post = db.query(Post).filter(
        Post.title == title, Post.owner_id == current_user.id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found!")
    db.delete(post)
    db.commit()
    return post


@user_router.post("/sign_up", status_code=status.HTTP_201_CREATED)
def sign_up(data: CreateUser, db: Session = Depends(get_db)):
    db_user: User = get_user(data.username, db)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered!")
    db_user: User = User(username=data.username,
                         hashed_password=hash_password(data.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: User = get_user(data.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password!")
    if not verify_password(data.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password!")
    access_token = create_access_token({"sub": str(user.username)})
    return {"access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id}
