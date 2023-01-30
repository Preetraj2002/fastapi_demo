from fastapi import APIRouter,HTTPException,status,Depends
from .. import schemas,models
from sqlalchemy.orm import Session
from ..database import get_db
from ..hashing import Hash


router= APIRouter()

@router.post('/user',response_model=schemas.ShowUser,tags=["Users"])
def create_user(request:schemas.User,db : Session= Depends(get_db)):
    hashedPassword = Hash.bcrypt(request.password)
    new_user= models.User(name=request.name,email=request.email,password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)        # refresh() method refreshes the connection and fetchs the most recent data
    return new_user


@router.get('/user/{id}',response_model=schemas.ShowUser,tags=["Users"])
def show_user(id,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not available")
    return user