from fastapi import APIRouter, Query, Depends, Response, status, HTTPException
from app.database import SessionLocal
from app.models import Rule
from .auth import get_current_user_from_request

rules_router = APIRouter()

@rules_router.get("/rules")
def get_rules(page: int = Query(default=1, ge=1), per_page: int = Query(default=25, ge=1), user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    rules = db.query(Rule).offset((page - 1) * per_page).limit(per_page).all()

    total_items = db.query(Rule).count()
    total_pages = (total_items + per_page - 1) // per_page

    return {
        "data": rules,
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_items": total_items
        }
    }

@rules_router.get("/rules/{rule_id}")
def get_rule(rule_id: int, user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    return rule

@rules_router.post("/rules")
def create_rule(request: dict, user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    rule = Rule(**request)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@rules_router.put("/rules/{rule_id}")
def update_rule(rule_id: int, request: dict, user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    for key, value in request.items():
        if key not in ["id", "created_at"]:
            setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return rule

@rules_router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int, user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    db.query(Rule).filter(Rule.id == rule_id).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
