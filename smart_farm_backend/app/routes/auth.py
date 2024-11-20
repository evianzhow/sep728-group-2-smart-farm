from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.database import SessionLocal
from app.models import User
from app.utils import hash_password, verify_password, create_session_token

auth_router = APIRouter()
security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials):
    db = SessionLocal()
    user = db.query(User).filter(User.username == credentials.username).first()
    db.close()
    if user and verify_password(credentials.password, user.password):
        return user
    raise HTTPException(status_code=401, detail="Invalid credentials")

@auth_router.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_current_user(credentials)
    token = create_session_token(user.username)
    return {"message": "Login successful", "token": token}
