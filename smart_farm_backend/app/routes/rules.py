from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Rule as RuleModel
from app.schemas import Rule as RuleSchema, RuleCreate
from .auth import get_current_user

rules_router = APIRouter()

@rules_router.get("/rules")
def get_rules(db: Session = Depends(SessionLocal), user=Depends(get_current_user)):
    return db.query(RuleModel).all()

@rules_router.post("/rules")
def create_rule(rule: RuleCreate, db: Session = Depends(SessionLocal), user=Depends(get_current_user)):
    db_rule = RuleModel(**rule.model_dump())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@rules_router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(SessionLocal), user=Depends(get_current_user)):
    rule = db.query(RuleModel).filter(RuleModel.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
    return {"message": "Rule deleted"}
