from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List             # Creates a collection of Pydantic classes
from .hashing import Hash
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)    # Whenever a database is not found it creates one

def get_db():
    db = SessionLocal()
    try:
        yield db    # similar to yield but it returns a generator object
    finally:
        db.close()

@app.get('/')
def home():
    return "welcome home"
@app.post("/blog",status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db: Session = Depends(get_db)): # the Depends function converts the Session obj into pydantic thing
                                                                # request in a Blog obj (one of the schemas)
    '''creating blog with user passed title and body'''

    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    # return f'creating blog with title:{request.title} and body:{request.body}'

@app.get('/blog',response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs= db.query(models.Blog).all()              # query for passing an search request
                                                    # all() fetches all the items in the database
    return blogs


@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog)
def show(id,response: Response,db: Session = Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()          # filter picks single entry from the database with a field like Blog.id
                                                                              # first() gives the sigle 1st entry found
    if blog == None:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")

    return blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)        # 204 is bound to return no content
def delete_blog(id,db : Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail":"deleted successfully"}

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)     # update a existing post
def update(id,request:schemas.Blog,db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} is not available")
    blog.update(request,synchronize_session=False)        # update() is a bulk operation
    db.commit()
    return {'detail':"Updated Successfully"}

@app.post('/user')
def create_user(request:schemas.User,db : Session= Depends(get_db)):
    hashedPassword = Hash.bcrypt(request.password)
    new_user= models.User(name=request.name,email=request.email,password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)        # refresh() method refreshes the connection and fetchs the most recent data
    return new_user









# if __name__=="__main__":
#     uvicorn.run(app,host="localhost",port=8080)