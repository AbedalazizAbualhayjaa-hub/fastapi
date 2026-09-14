from fastapi import Header, HTTPException


def get_current_user_id(authorization: str | None = Header(default=None)):
    if authorization is None or not authorization.startswith("Bearer user-"):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    try:
        return int(authorization.removeprefix("Bearer user-"))
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
