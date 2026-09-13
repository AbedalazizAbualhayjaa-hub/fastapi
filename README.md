# FastAPI Training Tasks

This repository contains my solutions for the FastAPI training tasks.

## Tasks

1. **Task 1 - Design the Contract**  
   Design REST endpoints for comments on a post, including the method, URL, and success status code.

2. **Task 2 - Hello, API**  
   Create a basic FastAPI app with a root endpoint and a `/greet/{name}` endpoint, then test both using the `/docs` page.

3. **Task 3 - Model the Data**  
   Create `UserCreate` and `UserOut` Pydantic models, validate the email and password, and make sure the password is never returned.

4. **Task 4 - Filter and Paginate**  
   Create a `GET /posts` endpoint with optional `published`, `limit`, and `offset` query parameters.

5. **Task 5 - Build CRUD for Users**  
   Build create, list, get, update, and delete endpoints for users with the correct status codes.

6. **Task 6 - A Shared Dependency**  
   Create a reusable pagination dependency and use it in two endpoints.

7. **Task 7 - Persist for Real**  
   Connect the posts API to a SQLite database using SQLAlchemy and make sure the data remains after restarting the server.

8. **Task 8 - Meaningful Failures**  
   Add proper error handling for missing users and duplicate emails.

9. **Task 9 - Protect an Endpoint**  
   Add token protection to create, update, and delete endpoints while keeping read endpoints public.

10. **Task 10 - Test the Contract**  
    Write pytest tests for successful creation, missing posts, invalid input, and reading a created post.

11. **Task 11 - A Complete Blog API**  
    Build a complete FastAPI blog API with users, posts, comments, validation, database support, authentication, error handling, testing, and documentation.

## Repository Structure

Each task is kept simple and separate. The solution file for each task can be opened directly from the main repository page.
