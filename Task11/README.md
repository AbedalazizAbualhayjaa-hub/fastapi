# Task 11 - Complete Blog API

This is a complete FastAPI blog backend with users, posts, comments, validation, SQLite storage, token authentication, authorization checks, error handling, tests, and automatic API documentation.

## Files

- `main.py` - API routes and CRUD operations
- `models.py` - SQLAlchemy database models
- `schemas.py` - Pydantic input and output models
- `database.py` - SQLite connection and `get_db` dependency
- `auth.py` - token authentication
- `test_main.py` - pytest tests

## Run

```bash
pip install -r requirements.txt
fastapi dev main.py
```

Open:

```text
http://127.0.0.1:8000/docs
```

The generated API schema includes the users, posts, and comments routes and their request and response models.

## Authentication

Create a user first. If the user ID is `1`, protected requests use:

```text
Authorization: Bearer user-1
```

Post creation, update, and deletion require a token. Only the post author can update or delete that post. Comment write operations also require a token.

## Test

```bash
pytest -q
```

Result:

```text
.......                                                                  [100%]
7 passed
```
