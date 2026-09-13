from fastapi import FastAPI, Query

app = FastAPI()

posts = [
    {"id": 1, "title": "First post", "published": True},
    {"id": 2, "title": "Second post", "published": False},
    {"id": 3, "title": "Third post", "published": True},
    {"id": 4, "title": "Fourth post", "published": False},
    {"id": 5, "title": "Fifth post", "published": True}
]

@app.get("/posts")
def list_posts(
    published: bool | None = Query(default=None),
    limit: int = 10,
    offset: int = 0
):
    result = posts

    if published is not None:
        result = [post for post in posts if post["published"] == published]

    return result[offset:offset + limit]
