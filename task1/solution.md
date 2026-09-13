# Task 1 - Design the Contract

| Operation | Method | URL | Status Code |
|---|---|---|---|
| List comments on a post | GET | `/posts/{post_id}/comments` | 200 OK |
| Add a comment to a post | POST | `/posts/{post_id}/comments` | 201 Created |
| Get one comment | GET | `/posts/{post_id}/comments/{comment_id}` | 200 OK |
| Delete one comment | DELETE | `/posts/{post_id}/comments/{comment_id}` | 204 No Content |
