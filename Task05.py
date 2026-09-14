from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr


users: dict[int, dict] = {}
next_id = 1


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global next_id
    new_user = {"id": next_id, **user.model_dump()}
    users[next_id] = new_user
    next_id += 1
    return new_user


@app.get("/users", response_model=list[UserOut])
def list_users():
    return list(users.values())


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserCreate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = {"id": user_id, **user.model_dump()}
    return users[user_id]


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
