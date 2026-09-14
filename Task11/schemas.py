from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr


class PostCreate(BaseModel):
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


class PostOut(BaseModel):
    id: int
    title: str
    body: str
    author_id: int
    author_name: str


class CommentCreate(BaseModel):
    body: str = Field(min_length=1)


class CommentOut(BaseModel):
    id: int
    body: str
    post_id: int
    author_id: int
    author_name: str
