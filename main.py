from fastapi import FastAPI
from services import post_router, user_router

app = FastAPI(
    title="Text Post App",
    docs_url="/documentation",
    redoc_url=None)

app.include_router(post_router)
app.include_router(user_router)


@app.get("/says")
def love():
    return {"muhammad": "I Love You MAEDEW."}


##### for local test ####
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
