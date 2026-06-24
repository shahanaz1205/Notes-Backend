from database import SessionLocal

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET_KEY = "ai_notes_secret_key"
ALGORITHM = "HS256"

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("TOKEN PAYLOAD =", payload)

        return payload

    except JWTError as e:
        print("JWT ERROR =", e)

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )


def get_admin_user(
    current_user=Depends(get_current_user)
):
    print("CURRENT USER =", current_user)

    role = current_user.get("role", "").lower()

    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access only"
        )

    return current_user