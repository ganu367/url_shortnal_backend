from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field
from typing import List


class UserBase(BaseModel):
    username: str
    email_address: EmailStr


class UserCreate(UserBase):
    password: str
    confirm_password: str

    class config:

        orm_mode = True


class UrlCreate(BaseModel):
    original_url: str


class UrlUpdateCount(BaseModel):
    click_count: int


class UrlUpdate(BaseModel):
    key_url: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user: Union[dict, None] = None
