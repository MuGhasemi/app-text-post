from pydantic import BaseModel


class Create_Post(BaseModel):
    title: str
    description: str


class Responce_Post(BaseModel):
    title: str
    description: str
