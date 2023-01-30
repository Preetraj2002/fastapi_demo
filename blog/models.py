# This file contains the user defined model or schema
# i.e. the structure of the database (sqlalchemy models are called models)

from sqlalchemy import Column,Integer,String,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

# DataBase for Blogs
class Blog(Base):
    __tablename__="blogs collection"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    body = Column(String)
    user_id=Column(Integer,ForeignKey("Users Info.id"))

    creator= relationship("User",back_populates="blogs")

# DataBase for Users
class User(Base):
    __tablename__="Users Info"
    id = Column(Integer,primary_key=True,index=True)
    name= Column(String)
    email= Column(String)
    password= Column(String)

    blogs=relationship("Blog",back_populates="creator")