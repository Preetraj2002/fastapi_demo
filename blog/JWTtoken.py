from datetime import datetime,timedelta
from typing import Union,Optional
from jose import JWTError,jwt

SECRET_KEY='c03776b462182add81ce2113c203b310e8c546e6651018a5bb63f7b6a343bd01'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt