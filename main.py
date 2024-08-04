from fastapi import FastAPI,Depends
from sqlmodel import select
from db import init_db,get_session
from models import User,UserCreate,Song
from contextlib import asynccontextmanager
from routers import UserRouter

init_db()
async def lifespan(app:FastAPI):
    init_db()
    yield
app =FastAPI(lifespan=lifespan)


@app.post("/make-song", response_model=Song)
def create_song(*, session=Depends(get_session))->Song:
    # user_obj = User(name=data.name, age=data.age, address=data.address)
    # session.add(user_obj)
    # session.commit()
    # session.refresh(user_obj)
    # return user_obj
    user=session.get(User,6)
    song_obj=Song(name='amke amar moton thakte dao',album='your true love',user_id=6,user=user)
    session.add(song_obj)
    session.commit()
    session.refresh(song_obj)
    return song_obj

@app.get("/songs")
def get_song(session=Depends(get_session))->list[Song]:
    state=select(Song)
    songs=session.exec(state).all()
    return songs

@app.get("/get-user")
def create_user(session=Depends(get_session)):
    state=select(User)
    song_user=session.exec(select(Song).where(Song.user_id=="6")).all()
    users=session.exec(state).all() 
    return song_user
   
@app.post("/create-user/{userID}", response_model=User)
def create_user(data: UserCreate, session=Depends(get_session)):
    user_obj = User(name=data.name, age=data.age, address=data.address)
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    return user_obj
app.include_router(UserRouter.router)
@app.get("/")
def root():
   return "server is running"


