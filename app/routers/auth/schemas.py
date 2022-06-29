from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    email: EmailStr
    password: str

class Register(BaseModel):
    email: EmailStr
    password: str
    username: str
    bio: str

class Token(BaseModel):
    access_token: str
    token_type: str
