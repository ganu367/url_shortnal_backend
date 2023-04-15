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


router = APIRouter(prefix="/api", tags=["Contact"])

get_db = database.get_db


@router.post("/contact-us")
def contactUs(contacts_fields: schemas.contactUsCreate, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(
        models.User.email == contacts_fields.email)

    if not get_user.first():
        user_id = None
    else:
        user_id = get_user.first().id

    try:
        new_message = models.CONTACTUS(
            **contacts_fields.dict(), user_id=user_id)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return {f"{contacts_fields.full_name} will reach as soon as possible"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig}")
