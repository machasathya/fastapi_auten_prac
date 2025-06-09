from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str


class PostCreate(BaseModel):
    id: int
    title: str
    context: str
    owner_id :int


class PostShow(PostCreate):
    title: str
    context: str


class UserShow(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCred(BaseModel):
    username: str
    Password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
