from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CreatePost(BaseModel):
    title: str
    description: str


class ResponcePost(BaseModel):
    id: UUID
    title: str
    description: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime


class UpdatePost(BaseModel):
    title: str | None = None
    description: str | None = None


class CreateUser(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: UUID
