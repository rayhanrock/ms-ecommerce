from fastapi import FastAPI
from item.routers import router as item_router
from inventory.routers import router as inventory_router
import database

app = FastAPI()

app.include_router(item_router)
app.include_router(inventory_router)


@app.get("/")
def root():
    return {"message": "Hello product service!"}
