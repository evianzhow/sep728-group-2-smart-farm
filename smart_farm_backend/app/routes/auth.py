from fastapi import APIRouter, HTTPException, Request
from fastapi.security import HTTPBasic
from app.database import SessionLocal
from app.models import User
from app.utils import hash_password, verify_password, create_session_token
auth_router = APIRouter()
security = HTTPBasic()

sessions = {} # In-memory session storage

def get_current_username_from_token(token: str):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    username = sessions.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

def username_to_user(username: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def validate_username_password(username: str, password: str):
    if not username or not password:
        raise HTTPException(status_code=400, detail="Missing username or password")
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def get_current_user_from_request(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    return username_to_user(get_current_username_from_token(token))

@auth_router.post("/login")
def login(credentials: dict):
    username = credentials.get("username")
    password = credentials.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="Missing username or password")
    user = validate_username_password(username, password)
    if user:
        token = create_session_token(user.username)
        sessions[token] = user.username
        return {"message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")
