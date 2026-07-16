#imports necessary libraries
from fastapi import Depends, FastAPI, HTTPException
from models.user import User
from sqlalchemy.orm import Session
from routers import auth, notes




#Create fastapi app 
app = FastAPI()


#Look at my models and create the tables in PostgreSQL
app.include_router(auth.router)
app.include_router(notes.router)


