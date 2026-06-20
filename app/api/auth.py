from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext

from app.schemas.auth_schema import RegisterRequest
from app.models.user import User
from app.database.connection import SessionLocal
from app.schemas.auth_schema import LoginRequest

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post("/register")
def register(request: RegisterRequest):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(
        request.password
    )

    new_user = User(
        full_name=request.full_name,
        email=request.email,
        phone=request.phone,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Registration Successful",
        "user_id": new_user.id,
        "email": new_user.email
    }
@router.post("/login")
def login(request: LoginRequest):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not pwd_context.verify(
        request.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login Successful",
        "user_id": user.id,
        "email": user.email
    }