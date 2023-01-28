import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"data":{"name":"Preetraj"}}

@app.get('/blog')
def index(limit=10,published:bool=True,sort:Optional[str]=None):
    if published:
        return {'data':f"{limit} published blogs from the db"}
    else :
        return  {'data':f"{limit}blogs from the db"}




@app.get("/blog/unpublished")
def unpublished():
    return {'data':'all unpublished data'}


@app.get("/blog/{id}")
def show(id):
    return {'data':id}




@app.get("/blog/{id}/comments")
def comments(id:int,limit=10):
    """fetch comments of blog with id = id"""
    return {"data":{"a","b"},'id':id,'docs':comments.__doc__,'limit':10}


class Blog(BaseModel):
    title:str
    body:Optional[str]=None

@app.post('/blog')
def create_blog(request:Blog):
    return {'data':"blog is created successfully",'json':request}

if __name__=="__main__":
    uvicorn.run(app,host='localhost',port=8000)
