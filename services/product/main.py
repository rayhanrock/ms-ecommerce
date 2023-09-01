from fastapi import FastAPI
from item.routers import router as item_router
import database

app = FastAPI()

app.include_router(item_router)


@app.get("/")
def root():
    return {"message": "Hello product service!"}
