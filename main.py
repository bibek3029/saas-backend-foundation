#imports necessary libraries
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database import engine, SessionLocal, Base, get_db
from models import User, Note
from sqlalchemy.orm import Session
from schemas import RegisterSchema, LoginSchema, NoteSchema


#Create fastapi app 
app = FastAPI()


#Look at my models and create the tables in PostgreSQL
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

#helper function to hash password

def hash_password(password: str):
    return pwd_context.hash(password)

#jwt secret key and algorithm
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
Session_Expires_Minutes = 30

# Helper for access token creation jwt
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Session_Expires_Minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
#verify access token 
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    
# register endpoint
@app.post("/register")
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
@app.post("/login")
def login_user(user: LoginSchema, db: Session = Depends(get_db)):
    stored_user = db.query(User).filter(User.email == user.email).first()
    if not stored_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not pwd_context.verify(user.password, stored_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# protected endpoints
@app.get("/profile")
def get_profile(token: str, db: Session = Depends(get_db)):
    email = verify_access_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "email": user.email}

# Note table endpoints
@app.post("/notes")
def create_note(note: NoteSchema,db: Session = Depends(get_db)):
                new_note = Note(title=note.title, content=note.content, user_id=1)  
                db.add(new_note)
                db.commit()
                db.refresh(new_note)
                return {"message": "Note created successfully", "note": new_note}


