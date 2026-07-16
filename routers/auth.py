from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database.database import get_db
from models.user import User
from schemas import RegisterSchema, LoginSchema
from core.security import (
    hash_password,
    create_access_token,
    verify_access_token
)



router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# register endpoint
@router.post("/register")
def register_user(user: RegisterSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "user registered successfully"}

# Login endpoint
@router.post("/login")
def login_user(user: LoginSchema, db: Session = Depends(get_db)):
    stored_user = db.query(User).filter(User.email == user.email).first()
    if not stored_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not pwd_context.verify(user.password, stored_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile")
def get_profile(token: str, db: Session = Depends(get_db)):
    email = verify_access_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "email": user.email}

@router.get("/current_user")
def get_current_user(token: str, db: Session = Depends(get_db)):
    email = verify_access_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
