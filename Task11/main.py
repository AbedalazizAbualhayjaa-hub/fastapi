from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from auth import get_current_user_id
from database import Base, engine, get_db
from models import Comment, Post, User
from schemas import CommentCreate, CommentOut, PostCreate, PostOut, UserCreate, UserOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task 11 Blog API")


def user_out(user: User):
    return UserOut(id=user.id, name=user.name, email=user.email)


def post_out(post: Post):
    return PostOut(
        id=post.id,
        title=post.title,
        body=post.body,
        author_id=post.author_id,
        author_name=post.author.name
    )


def comment_out(comment: Comment):
    return CommentOut(
        id=comment.id,
        body=comment.body,
        post_id=comment.post_id,
        author_id=comment.author_id,
        author_name=comment.author.name
    )


def require_user(db: Session, user_id: int):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid user token")
    return user


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_out(user)


@app.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return [user_out(user) for user in db.query(User).all()]


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_out(user)


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    data: UserCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    require_user(db, current_user_id)
    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    duplicate = db.query(User).filter(User.email == data.email, User.id != user_id).first()
    if duplicate:
        raise HTTPException(status_code=409, detail="Email already exists")

    user.name = data.name
    user.email = data.email
    user.password = data.password
    db.commit()
    db.refresh(user)
    return user_out(user)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    require_user(db, current_user_id)
    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(user)
    db.commit()


@app.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    data: PostCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = require_user(db, current_user_id)
    post = Post(**data.model_dump(), author_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    post.author = user
    return post_out(post)


@app.get("/posts", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).options(joinedload(Post.author)).all()
    return [post_out(post) for post in posts]


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).options(joinedload(Post.author)).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_out(post)


@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    data: PostCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    post = db.query(Post).options(joinedload(Post.author)).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    require_user(db, current_user_id)
    if post.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="Only the post author can edit this post")

    post.title = data.title
    post.body = data.body
    db.commit()
    db.refresh(post)
    return post_out(post)


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    require_user(db, current_user_id)
    if post.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="Only the post author can delete this post")

    db.delete(post)
    db.commit()


@app.post(
    "/posts/{post_id}/comments",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    post_id: int,
    data: CommentCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if db.get(Post, post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")
    user = require_user(db, current_user_id)

    comment = Comment(body=data.body, post_id=post_id, author_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    comment.author = user
    return comment_out(comment)


@app.get("/posts/{post_id}/comments", response_model=list[CommentOut])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    if db.get(Post, post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = (
        db.query(Comment)
        .options(joinedload(Comment.author))
        .filter(Comment.post_id == post_id)
        .all()
    )
    return [comment_out(comment) for comment in comments]


@app.get("/posts/{post_id}/comments/{comment_id}", response_model=CommentOut)
def get_comment(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    comment = (
        db.query(Comment)
        .options(joinedload(Comment.author))
        .filter(Comment.id == comment_id, Comment.post_id == post_id)
        .first()
    )
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment_out(comment)


@app.put("/posts/{post_id}/comments/{comment_id}", response_model=CommentOut)
def update_comment(
    post_id: int,
    comment_id: int,
    data: CommentCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    comment = (
        db.query(Comment)
        .options(joinedload(Comment.author))
        .filter(Comment.id == comment_id, Comment.post_id == post_id)
        .first()
    )
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    require_user(db, current_user_id)
    if comment.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    comment.body = data.body
    db.commit()
    db.refresh(comment)
    return comment_out(comment)


@app.delete(
    "/posts/{post_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_comment(
    post_id: int,
    comment_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.post_id == post_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    require_user(db, current_user_id)
    if comment.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(comment)
    db.commit()
