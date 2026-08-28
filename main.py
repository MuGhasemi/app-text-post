from fastapi import FastAPI
from services import router

app = FastAPI(
    title="Text Post App",
    docs_url="/documentation",
    redoc_url=None)

app.include_router(router)

##### for local test ####
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
