from pydantic import BaseModel
from uuid import UUID


class Create_Post(BaseModel):
    title: str
    description: str


class Responce_Post(BaseModel):
    id: UUID
    title: str
    description: str
