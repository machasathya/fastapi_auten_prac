from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import null
from database import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(50))
    context = Column(String(50))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50))
    password = Column(String(50))


class Like(Base):
    __tablename__ = "likes"
    post_id = Column(Integer,ForeignKey("posts.id",ondelete='CASCADE'),primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)