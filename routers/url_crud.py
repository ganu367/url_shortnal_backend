from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from fastapi.responses import RedirectResponse
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


router = APIRouter(prefix="/api", tags=["URL"])

get_db = database.get_db


@router.post("/home/create-url-short")
def createUShort(url_fields: schemas.UrlCreate, db: Session = Depends(get_db)):
    get_url = db.query(models.URL).filter(
        models.URL.target_url == url_fields.original_url)

    if not validators.url(url_fields.original_url):
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, detail="Enter a valid url")

    else:
        # generate random string(8)
        key_string = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase +
                                            string.digits, k=6))
        secret_key = "".join(secrets.choice(key_string) for _ in range(8))
        try:
            new_short_url = models.URL(
                target_url=url_fields.original_url, key=key_string, secrete_key=secret_key)
            db.add(new_short_url)
            db.commit()
            db.url = key_string
            db.refresh(new_short_url)
            return new_short_url
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig}")


@router.post("/home/create")
def createUrlShort(url_fields: schemas.UrlCreate, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user = current_user
    username = current_user.user['username']

    get_url = db.query(models.URL).filter(
        models.URL.target_url == url_fields.original_url)
    get_user = db.query(models.User).filter(models.User.username == username)

    if not validators.url(url_fields.original_url):

        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, detail="Enter a valid url")
    else:
        if (get_user.first().is_active == True):

            # generate random string(8)
            key_string = ''.join(random.choices(
                string.ascii_lowercase + string.digits + string.ascii_uppercase, k=8))
            secret_key = "".join(secrets.choice(key_string) for _ in range(8))

            try:
                new_short_url = models.URL(
                    target_url=url_fields.original_url, key=key_string, secrete_key=secret_key, created_by=username, user_id=get_user.first().id)

                db.add(new_short_url)
                db.commit()
                db.url = key_string
                db.refresh(new_short_url)

                return new_short_url

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig}")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"{username} not found")


@router.get("/get-all-url")
def allUrl(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user = current_user
    username = current_user.user['username']

    get_user = db.query(models.User).filter(models.User.username == username)

    if (get_user.first().is_active == True):
        try:
            all_links = db.query(models.URL).filter(
                models.URL.user_id == get_user.first().id, models.URL.is_active == True).all()
            return all_links
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig}")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{username} not found")


@router.put("/custom-url/{url_id}")
def customUrl(url_id: int, url_fields: schemas.UrlUpdate, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user = current_user
    username = current_user.user['username']
    get_user = db.query(models.User).filter(models.User.username == username)

    get_url = db.query(models.URL).filter(
        models.URL.id == url_id, models.URL.user_id == get_user.first().id, models.URL.is_active == True)

    if not get_url.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="not found")

    else:
        if (get_user.first().is_active == True):

            # generate random string(8)
            # key_string = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase  +
            #                                     string.digits, k=6))
            # secret_key = "".join(secrets.choice(key_string) for _ in range(8))

            try:
                get_url.update(
                    {"key": url_fields.key_url, "modified_by": username})

                db.commit()

                return get_url.first()

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig}")

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"{username} not found")


@router.put("/delete-url/{url_id}")
def deleteLinked(url_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user = current_user
    username = current_user.user['username']

    get_user = db.query(models.User).filter(models.User.username == username)

    if (get_user.first().is_active == True):
        try:

            db.query(models.URL).filter(models.URL.id == url_id, models.URL.user_id == get_user.first(
            ).id, models.URL.is_active == True).update({"is_active": False, "modified_by": username})
            db.commit()

            return {"This link is deleted"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig}")
