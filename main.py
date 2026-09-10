from fastapi import FastAPI
from services import post_router, user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Text Post App",
    docs_url="/documentation",
    redoc_url=None)

app.include_router(post_router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://app-text-post-frontend.onrender.com"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


##### for local test ####
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
