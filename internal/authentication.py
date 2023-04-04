from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import database
import models
import hashing
import tokens
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

get_db = database.get_db


@router.post("/login")
def loginUser(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    val_user = db.query(models.User).filter(
        models.User.username == request.username)

    if not val_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The user does not exists")
    else:
        # verify password between requesting by a user & database password
        if not hashing.Hash.verify(val_user.first().password, request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Incorrect Passwords")
        else:
            if val_user.first().is_admin == False:

                access_token = tokens.create_access_token(data={"user": {
                    "username": request.username, "email_address": val_user.first().email_address, "isAdmin": val_user.first().is_admin}})
                return {"access_token": access_token, "token_type": "bearer"}

            else:
                access_token = tokens.create_access_token(data={"user": {
                    "username": request.username, "isAdmin": val_user.first().is_admin}})
                return {"access_token": access_token, "token_type": "bearer"}
