from fastapi import FastAPI
from order.routers import router as order_router
import database


app = FastAPI()
app.include_router(order_router)


@app.get("/")
def root():
    return {"message": f"Hello Order!"}
