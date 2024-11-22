from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Rule as RuleModel
from app.schemas import Rule as RuleSchema, RuleCreate
from .auth import get_current_user_from_request

rules_router = APIRouter()

@rules_router.get("/rules")
def get_rules(user=Depends(get_current_user_from_request)):
    # FIXME
    #def get_rules(db: Session = Depends(SessionLocal), user=Depends(get_current_user_from_request)):
    # return db.query(RuleModel).all()
    return {"message": "Rules fetched"}


@rules_router.get("/rules/{rule_id}")
def get_rule(rule_id: int, db: Session = Depends(SessionLocal), user=Depends(get_current_user_from_request)):
    # FIXME
    return {"message": "Rule fetched"}

@rules_router.post("/rules")
def create_rule(rule: RuleCreate, db: Session = Depends(SessionLocal), user=Depends(get_current_user_from_request)):
    db_rule = RuleModel(**rule.model_dump())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@rules_router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(SessionLocal), user=Depends(get_current_user_from_request)):
    rule = db.query(RuleModel).filter(RuleModel.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
    return {"message": "Rule deleted"}
