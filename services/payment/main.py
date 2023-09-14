from fastapi import FastAPI
from payment_app.routers import router as payment_router
import database

app = FastAPI()
app.include_router(payment_router)


@app.get("/")
def root():
    return {"message": f"Hello payment service!"}
