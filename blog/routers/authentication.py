from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import schemas,database,models
from ..hashing import Hasher

router = APIRouter(
    tags=["Auth"],
    prefix="/login"
)

@router.post("/")
def login(request:schemas.Login,db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials !! User with id {request.username} not available in the database")

    matching = Hasher.verify_password(request.password,user.password)

    if not matching:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect Password")
    return user