from fastapi import FastAPI
from .schemas import Responce_Post, Create_Post


app = FastAPI(
    title="Text Post App",
    docs_url="/documentation",
    redoc_url=None)

posts: dict = {1: {"title": "hello-world", "description": "I'm here...!"}}


@app.get("/posts")
def get_posts():
    return posts


@app.get("/posts/{id}")
def get_post_by_id(id: int) -> Responce_Post:
    return posts[id]


@app.post("/posts/new")
def create_new_post(data: Create_Post) -> dict:
    num = max(posts.keys())+1
    posts[num] = data.model_dump()
    return {"posts" : posts}


@app.put("/posts/{id}")
def update_post(id: int):
    pass


@app.delete("/posts/{id}")
def delete_post(id: int):
    pass
