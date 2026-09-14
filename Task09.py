from fastapi import FastAPI, Depends, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class PostCreate(BaseModel):
    title: str
    body: str


posts: dict[int, dict] = {}
next_id = 1


def require_token(authorization: str | None = Header(default=None)):
    if authorization != "Bearer secret-token":
        raise HTTPException(status_code=401, detail="Invalid or missing token")


@app.get("/posts")
def list_posts():
    return list(posts.values())


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = posts.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, _: None = Depends(require_token)):
    global next_id
    new_post = {"id": next_id, **post.model_dump()}
    posts[next_id] = new_post
    next_id += 1
    return new_post


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: PostCreate, _: None = Depends(require_token)):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    posts[post_id] = {"id": post_id, **post.model_dump()}
    return posts[post_id]


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, _: None = Depends(require_token)):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts[post_id]
