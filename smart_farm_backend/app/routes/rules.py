from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Rule
from app.auth import get_current_user

rules_router = APIRouter()

@rules_router.get("/rules")
def get_rules(db: Session = Depends(SessionLocal), user=Depends(get_current_user)):
    return db.query(Rule).all()

@rules_router.post("/rules")
def create_rule(rule: Rule, db: Session = Depends(SessionLocal), user=Depends(get_current_user)):
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@rules_router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(SessionLocal), user=Depends(get_current_user)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
    return {"message": "Rule deleted"}
