from fastapi import FastAPI
from shopping_cart.routers import router as shopping_cart_router
import database
database.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
app.include_router(shopping_cart_router)


@app.get("/")
def root():
    return {"message": f"Hello cart!"}
