import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_user(name="Ali", email="ali@example.com"):
    return client.post(
        "/users",
        json={"name": name, "email": email, "password": "password123"}
    )


def test_create_user_hides_password():
    response = create_user()
    assert response.status_code == 201
    assert "password" not in response.json()


def test_duplicate_email_returns_409():
    create_user()
    response = create_user(name="Another Ali")
    assert response.status_code == 409


def test_missing_user_returns_404():
    response = client.get("/users/999")
    assert response.status_code == 404


def test_post_write_requires_token():
    response = client.post("/posts", json={"title": "Hello", "body": "Post body"})
    assert response.status_code == 401


def test_post_author_can_create_read_update_and_delete():
    create_user()
    headers = {"Authorization": "Bearer user-1"}

    create_response = client.post(
        "/posts",
        json={"title": "Hello", "body": "Post body"},
        headers=headers
    )
    assert create_response.status_code == 201
    post_id = create_response.json()["id"]

    read_response = client.get(f"/posts/{post_id}")
    assert read_response.status_code == 200
    assert read_response.json()["author_name"] == "Ali"

    update_response = client.put(
        f"/posts/{post_id}",
        json={"title": "Updated", "body": "Updated body"},
        headers=headers
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated"

    delete_response = client.delete(f"/posts/{post_id}", headers=headers)
    assert delete_response.status_code == 204


def test_non_author_cannot_edit_post():
    create_user()
    create_user(name="Sara", email="sara@example.com")

    create_response = client.post(
        "/posts",
        json={"title": "Hello", "body": "Post body"},
        headers={"Authorization": "Bearer user-1"}
    )
    post_id = create_response.json()["id"]

    response = client.put(
        f"/posts/{post_id}",
        json={"title": "Changed", "body": "Changed"},
        headers={"Authorization": "Bearer user-2"}
    )
    assert response.status_code == 403


def test_comment_crud():
    create_user()
    headers = {"Authorization": "Bearer user-1"}

    post_response = client.post(
        "/posts",
        json={"title": "Hello", "body": "Post body"},
        headers=headers
    )
    post_id = post_response.json()["id"]

    comment_response = client.post(
        f"/posts/{post_id}/comments",
        json={"body": "Nice post"},
        headers=headers
    )
    assert comment_response.status_code == 201
    comment_id = comment_response.json()["id"]

    list_response = client.get(f"/posts/{post_id}/comments")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/posts/{post_id}/comments/{comment_id}",
        json={"body": "Updated comment"},
        headers=headers
    )
    assert update_response.status_code == 200

    delete_response = client.delete(
        f"/posts/{post_id}/comments/{comment_id}",
        headers=headers
    )
    assert delete_response.status_code == 204
