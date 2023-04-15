from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import database
import schemas
import models
import string
import random
import secrets
import validators
import oauth2
# import requests


router = APIRouter(prefix="/api", tags=["User"])

get_db = database.get_db


@router.get("/get-all-users")
def allUser(db: Session = Depends(get_db), current_user: schemas.UrlCreate = Depends(oauth2.get_current_user)):
    current_user = current_user
    username = current_user.user['email_address']
    isAdmin = current_user.user['isAdmin']

    if (isAdmin != True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You can't access this page")
    else:
        val_user = db.query(models.User).filter(
            models.User.is_active == True, models.User.is_admin == False)
        if not val_user.count() == 0:
            return val_user.all()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.get("/delete-user/{user_id}")
def deleteUser(user_id: int, db: Session = Depends(get_db), current_user: schemas.UrlCreate = Depends(oauth2.get_current_user)):
    current_user = current_user
    username = current_user.user['email_address']
    isAdmin = current_user.user['isAdmin']

    if (isAdmin != True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You can't access this page")
    else:
        #3 user id
        val_user = db.query(models.User).filter(models.User.id == user_id).filter(
            models.User.is_active == True, models.User.is_admin == False)

        if val_user.first():
            val_user.update({"is_active": False,"is_deleted":False})
            db.commit()
            return {"This user is deleted."}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
