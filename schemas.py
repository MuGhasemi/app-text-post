from pydantic import BaseModel
from uuid import UUID


class CreatePost(BaseModel):
    title: str
    description: str
    owner_id: UUID


class ResponcePost(BaseModel):
    id: UUID
    title: str
    description: str
    owner_id: UUID


class UpdatePost(BaseModel):
    title: str | None = None
    description: str | None = None


class CreateUser(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
