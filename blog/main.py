from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blogs,users,authentication     # importing routes from router dir
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)    # Whenever a database is not found it creates one

app.include_router(blogs.router)
app.include_router(users.router)
app.include_router(authentication.router)


@app.get('/')
def home():
    return "welcome home"










# if __name__=="__main__":
#     uvicorn.run(app,host="localhost",port=8080)