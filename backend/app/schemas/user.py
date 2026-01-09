from pydantic import BaseModel, EmailStr

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

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
