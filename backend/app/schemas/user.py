from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserAdminOut(BaseModel):
    # Currently only being used to list out all users (an admin privilege)
    model_config = {"from_attributes": True}

    id: int
    email: EmailStr
    username: str
    is_admin: bool

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    email: EmailStr
    username: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    current_password: str | None = None  # required when changing email

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class DeleteAccount(BaseModel):
    current_password: str
