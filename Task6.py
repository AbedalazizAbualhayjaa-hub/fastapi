from fastapi import FastAPI, Depends

app = FastAPI()

posts = [
    {"id": 1, "title": "First post"},
    {"id": 2, "title": "Second post"},
    {"id": 3, "title": "Third post"},
    {"id": 4, "title": "Fourth post"}
]

users = [
    {"id": 1, "name": "Ali"},
    {"id": 2, "name": "Sara"},
    {"id": 3, "name": "Omar"},
    {"id": 4, "name": "Lina"}
]


def pagination(limit: int = 10, offset: int = 0):
    return {"limit": limit, "offset": offset}


@app.get("/posts")
def list_posts(page: dict = Depends(pagination)):
    start = page["offset"]
    end = start + page["limit"]
    return posts[start:end]


@app.get("/users")
def list_users(page: dict = Depends(pagination)):
    start = page["offset"]
    end = start + page["limit"]
    return users[start:end]
