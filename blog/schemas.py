# Response model also called response schemas
# Data-driven classes
# Pydantic is a data validation module
# Pydantic models are called Schemas


from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    body:str

class ShowBlog(BaseModel):
    title:str
    body:str
    class Config():
        orm_mode=True


class User(BaseModel):
    name:str
    email:str
    password:str