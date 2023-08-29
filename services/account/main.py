from fastapi import FastAPI
from users.routers import router as users_router
from auth.routers import router as auth_router
import database

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": f"Hello account !"}
