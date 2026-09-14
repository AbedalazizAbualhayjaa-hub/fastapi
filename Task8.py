from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr


users: dict[int, dict] = {}
next_id = 1


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global next_id

    for existing_user in users.values():
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=409, detail="Email already exists")

    new_user = {"id": next_id, **user.model_dump()}
    users[next_id] = new_user
    next_id += 1
    return new_user


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
