from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import database
import schemas
import models
import hashing
import tokens
import oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

get_db = database.get_db


@router.post("/create-user")
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    val_user = db.query(models.User).filter(
        models.User.username == request.username)
    if not len(request.username) >= 8:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail=f"{request.username} length must be gretter than 8 character.")
    else:
        # if not val_user.first():
            if (request.password == request.confirm_password):
                try:

                    new_user = models.User(username=request.username, email_address=request.email_address, created_by=request.username,
                                           password=hashing.Hash.bcrypt(request.password))
                    db.add(new_user)
                    db.commit()
                    db.refresh(new_user)

                    access_token = tokens.create_access_token(data={"user": {
                        "username": request.username, "email_address": request.email_address, "isAdmin": False}})

                    return {"access_token": access_token, "token_type": "bearer"}

                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(e.orig)}")
            else:
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"Password does not match")
        # else:
        #     raise HTTPException(status_code=status.HTTP_302_FOUND,
        #                         detail=f"{request.username} already exists.")
