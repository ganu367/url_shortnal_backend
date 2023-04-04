from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from internal import authentication, registration
from routers import url_crud, utility

models.Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.include_router(authentication.router)
app.include_router(registration.router)
app.include_router(url_crud.router)
app.include_router(utility.router)
