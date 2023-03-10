from typing import List                 # Creates a collection of Pydantic classes
from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas,models
from sqlalchemy.orm import Session
from ..database import get_db
from ..OAuth2 import get_current_user




router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
                                                                # the Depends function converts the Session obj into pydantic thing
                                                                # request in a Blog obj (one of the schemas)
    '''creating blog with user passed title and body'''

    new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    # return f'creating blog with title:{request.title} and body:{request.body}'

@router.get('/',response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):      # get current user applies lock to the endpoint
    blogs= db.query(models.Blog).all()              # query for passing an search request
                                                    # all() fetches all the items in the database
    return blogs


@router.get('/{id}',status_code=200,response_model=schemas.ShowBlog)
def show_blog(id,db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()          # filter picks single entry from the database with a field like Blog.id
                                                                              # first() gives the sigle 1st entry found
    if blog == None:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")

    return blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)        # 204 is bound to return no content
def delete_blog(id,db : Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail":"deleted successfully"}

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)     # update a existing post
def update(id,request:schemas.Blog,db:Session= Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} is not available")
    blog.update(request,synchronize_session=False)        # update() is a bulk operation
    db.commit()
    return {'detail':"Updated Successfully"}