# FastAPI Training Tasks

## Tasks

1. [Task 1 - Design the Contract](Task1.md)  
   Design REST endpoints for comments on a post, including the method, URL, and success status code.

2. [Task 2 - Hello, API](Task2.py)  
   Create a basic FastAPI app with a root endpoint and a `/greet/{name}` endpoint, then test both using the `/docs` page.

3. [Task 3 - Model the Data](Task3.py)  
   Create `UserCreate` and `UserOut` Pydantic models, validate the email and password, and make sure the password is never returned.

4. [Task 4 - Filter and Paginate](Task4.py)  
   Create a `GET /posts` endpoint with optional `published`, `limit`, and `offset` query parameters.

5. [Task 5 - Build CRUD for Users](Task5.py)  
   Build create, list, get, update, and delete endpoints for users with the correct status codes.

6. [Task 6 - A Shared Dependency](Task6.py)  
   Create a reusable pagination dependency and use it in two endpoints.

7. [Task 7 - Persist for Real](Task7.py)  
   Connect the posts API to a SQLite database using SQLAlchemy and make sure the data remains after restarting the server.

8. [Task 8 - Meaningful Failures](Task8.py)  
   Add proper error handling for missing users and duplicate emails.

9. **Task 9 - Protect an Endpoint**  
   Add token protection to create, update, and delete endpoints while keeping read endpoints public.

10. **Task 10 - Test the Contract**  
    Write pytest tests for successful creation, missing posts, invalid input, and reading a created post.

11. **Task 11 - A Complete Blog API**  
    Build a complete FastAPI blog API with users, posts, comments, validation, database support, authentication, error handling, testing, and documentation.

## Task 2 Docs Note

The `/docs` page shows both `GET /` and `GET /greet/{name}`. It also lets me test the endpoints directly and shows the JSON response returned by each one.

## Task 3 Note

The password is included in `UserCreate` because the user sends it when creating an account. It is not included in `UserOut` so the password is never returned in API responses.

## Task 4 Examples

- `/posts`
- `/posts?published=true`
- `/posts?limit=2&offset=1`
- `/posts?published=false&limit=1&offset=0`

Sending a value such as `/posts?limit=abc` returns a validation error because `limit` must be an integer.

## Task 5 Test Log

- `POST /users` returns `201 Created` and creates a user.
- `GET /users` returns `200 OK` and lists the users.
- `GET /users/1` returns `200 OK` when the user exists.
- `PUT /users/1` returns `200 OK` and updates the user.
- `DELETE /users/1` returns `204 No Content` and deletes the user.
- Requesting a missing user returns `404 Not Found`.

## Task 7 Check

The data is stored in `task7.db`, so it remains after restarting the server. SQL logging is enabled with `echo=True`. The posts list uses `selectinload` to load authors without running one extra query for every post.

## Task 8 Error Responses

Missing user:

```json
{
  "detail": "User not found"
}
```

Duplicate email:

```json
{
  "detail": "Email already exists"
}
```
