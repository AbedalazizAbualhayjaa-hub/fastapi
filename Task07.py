from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship, selectinload

app = FastAPI()

DATABASE_URL = "sqlite:///./task7.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="posts")


Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


class PostOut(BaseModel):
    id: int
    title: str
    body: str
    author_id: int

    model_config = {"from_attributes": True}


class PostWithAuthor(BaseModel):
    id: int
    title: str
    body: str
    author_name: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    author = db.get(User, post.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts", response_model=list[PostWithAuthor])
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).options(selectinload(Post.author)).all()
    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "author_name": post.author.name
        }
        for post in posts
    ]


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, data: PostCreate, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    author = db.get(User, data.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    post.title = data.title
    post.body = data.body
    post.author_id = data.author_id
    db.commit()
    db.refresh(post)
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
