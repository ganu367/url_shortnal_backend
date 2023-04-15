from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import database
import models
import hashing
import tokens
import schemas
import oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

get_db = database.get_db


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    val_user = db.query(models.User).filter(
        models.User.email_address == request.username)

    if not val_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User does not exists")
    else:
        # verify password between requesting by a user & database password
        if not hashing.Hash.verify(val_user.first().password, request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Incorrect Passwords")
        else:
            access_token = tokens.create_access_token(data={"user": {
                "email_address": val_user.first().email_address, "isAdmin": val_user.first().is_admin}})
            return {"access_token": access_token, "token_type": "bearer"}


@router.put("/update-password", status_code=status.HTTP_202_ACCEPTED)
def updatePassword(request: schemas.UserPassword, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(oauth2.get_current_user)):
    _username_ = current_user.user["email_address"]

    val_user = db.query(models.User).filter(
        models.User.email_address == _username_).first()

    if not val_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    else:
        if not hashing.Hash.verify(val_user.password, request.current_password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Incorrect Passwords")

        elif (request.new_password != request.confirm_password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Password not matched")

        else:

            db.query(models.User).filter(models.User.email_address == _username_).update(
                {"password": hashing.Hash.bcrypt(request.new_password)})
            db.commit()

            return {f"Password successfully updated"}


@router.put("/forget-password/{username}", status_code=status.HTTP_202_ACCEPTED)
def forgetPassword(username: str, request: schemas.ForgetPassword, db: Session = Depends(get_db)):
    val_user = db.query(models.User).filter(
        models.User.email_address == username).first()

    if not val_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    else:
        # email verification to send that perticular a user
        if (request.new_password != request.confirm_password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Password not matched")
        else:
            db.query(models.User).filter(models.User.email_address == username).update(
                {"password": hashing.Hash.bcrypt(request.new_password)})
            db.commit()
            return {f"Password successfully updated"}
