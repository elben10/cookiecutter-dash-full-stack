from typing import Optional

from pydantic import BaseModel, EmailStr, constr, validator


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

    @validator("full_name", pre=True)
    def passwords_match(cls, v, values, **kwargs):
        if v == "":
            return None
        return v


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: constr(strict=True, min_length=8)
    password2: constr(strict=True, min_length=8)

    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if values.get("password") != v:
            raise ValueError("Repeated password doensn't match")
        return v


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[constr(strict=True, min_length=8)] = None
    password2: Optional[constr(strict=True, min_length=8)] = None

    @validator("password", pre=True)
    def password_pre(cls, v, values, **kwargs):
        if v == "":
            return None
        return v

    @validator("password2", pre=True)
    def password2_pre(cls, v, values, **kwargs):
        if v == "":
            return None
        return v

    @validator("password2")
    def passwords2_match(cls, v, values, **kwargs):
        password = values.get("password")
        if (password or v) and (v != password):
            raise ValueError("Repeated password doensn't match")
        return v


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
