from sqlmodel import SQLModel,Field,Relationship
from pydantic import BaseModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password:str 
    songs: list['Song'] = Relationship(back_populates='user')

class Token(BaseModel):
    accesstoken:str
    token_type:str

class Song(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    name:str
    album:str
    user_id:int | None = Field(default=None,foreign_key='user.id')
    user:User=Relationship(back_populates='songs')
    

class UserCreate(SQLModel):
      email:str
      password:str
    