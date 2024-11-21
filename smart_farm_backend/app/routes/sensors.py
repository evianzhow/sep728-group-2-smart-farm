from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Rule
from .auth import get_current_user

sensors_router = APIRouter()
