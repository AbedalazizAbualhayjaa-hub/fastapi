from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class PostCreate(BaseModel):
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


posts: dict[int, dict] = {}
next_id = 1


@app.post("/posts", status_code=201)
def create_post(post: PostCreate):
    global next_id
    new_post = {"id": next_id, **post.model_dump()}
    posts[next_id] = new_post
    next_id += 1
    return new_post


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = posts.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


client = TestClient(app)


def setup_function():
    global next_id
    posts.clear()
    next_id = 1


def test_create_post():
    response = client.post("/posts", json={"title": "Hello", "body": "First post"})
    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_missing_post():
    response = client.get("/posts/999")
    assert response.status_code == 404


def test_invalid_input():
    response = client.post("/posts", json={"title": "", "body": ""})
    assert response.status_code == 422


def test_created_post_can_be_read():
    create_response = client.post("/posts", json={"title": "Hello", "body": "First post"})
    post_id = create_response.json()["id"]

    read_response = client.get(f"/posts/{post_id}")
    assert read_response.status_code == 200
    assert read_response.json()["title"] == "Hello"
