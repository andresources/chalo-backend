from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.database.connection import engine
from app.models.user import User

User.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

@app.get("/")
def home():
    return {
        "message": "Chalo Backend Running"
    }