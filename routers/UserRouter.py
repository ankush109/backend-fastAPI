from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlmodel import SQLModel, select, Session
from db import init_db, get_session
from models import User, UserCreate
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from Oauth import create_token
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register")
def register(userdata: UserCreate, session: Session = Depends(get_session)):
    logger.info(f"Attempting to register user with email: {userdata.email}")
    user_obj = User(
        email=userdata.email,
        password=get_password_hash(userdata.password)
    )
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    logger.info(f"User registered: {user_obj}")

    if user_obj is None:
        logger.error("Failed to register user")
        raise HTTPException(status_code=404, detail="Failed to register")
    return {
        "success": True,
        "user": user_obj
    }

@router.post("/login")
def login(userdata: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    email = userdata.username
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    
    
    if user is None:
        raise HTTPException(status_code=401, detail="No user found")
    
    if not verify_password(userdata.password, user.password):
        raise HTTPException(status_code=401, detail="Unauthorized / Invalid credentials")
    
    access_token = create_token(data={
        "user_id": user.id
    })
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
