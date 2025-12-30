from pydantic import BaseModel, EmailStr


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
