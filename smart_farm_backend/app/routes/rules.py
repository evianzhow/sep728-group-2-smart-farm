from fastapi import APIRouter, Query, Depends, Response, status, HTTPException
from app.database import SessionLocal
from app.models import Rule, EventLog
from .auth import get_current_user_from_request
from app.utils import convert_datetime_to_iso8601
from app.models import get_db
from sqlalchemy.orm import Session

rules_router = APIRouter()

@rules_router.get("/rules")
def get_rules(page: int = Query(default=1, ge=1), per_page: int = Query(default=25, ge=1), db: Session = Depends(get_db), _=Depends(get_current_user_from_request)):
    rules = db.query(Rule).offset((page - 1) * per_page).limit(per_page).all()

    for rule in rules:
        rule.created_at = convert_datetime_to_iso8601(rule.created_at)

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
def get_rule(rule_id: int, db: Session = Depends(get_db), _=Depends(get_current_user_from_request)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if rule is not None:
        rule.created_at = convert_datetime_to_iso8601(rule.created_at)
    return rule

def validate_rule(request: dict):
    trigger_sensor = request.get("trigger_sensor").lower()
    type = request.get("type").lower()
    op = request.get("op").lower()
    threshold = request.get("threshold")
    target_controller = request.get("target_controller").lower()
    action = request.get("action").lower()

    if type not in ["threshold", "event"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid rule type")
    if trigger_sensor not in ["steam.value", "steam.percentage", "dht11.humidity", "dht11.temperature.celsius", 
                              "dht11.temperature.fahrenheit", "dht11.temperature.kelvin", "dht11.dewpoint.celsius", 
                              "soil.value", "soil.percentage", "water.value", "water.percentage", "ultrasonic.value", 
                              "light.value", "light.percentage", "button", "pir", "relay", "led", "servo"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid trigger sensor")
    if target_controller not in ["buzzer", "fan", "relay", "led", "servo", "lcd"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid target controller")
    if type == "threshold" and op not in [">", ">=", "<", "<=", "==", "!="]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operator")
    if type == "threshold" and not threshold:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Threshold is required")
    if type == "event":
        if trigger_sensor == "button":
            if op not in ["pressed", "released"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operator")
        elif trigger_sensor == "pir":
            if op not in ["detected", "not-detected"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operator")
        elif trigger_sensor == "relay" or trigger_sensor == "led":
            if op not in ["active", "inactive"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operator")
        elif trigger_sensor == "servo":
            if op not in ["open", "half_open", "closed"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operator")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operator")
    if not all(kv.count('=') == 1 for kv in request.get('action', '').split(';') if kv):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action format. Must be key=value pairs separated by semicolons")
    # Save with lower case values
    return {**request, "trigger_sensor": trigger_sensor, "type": type, "op": op, "target_controller": target_controller, "action": action}

@rules_router.post("/rules")
def create_rule(request: dict, db: Session = Depends(get_db), _=Depends(get_current_user_from_request)):
    validated_request = validate_rule(request)
    rule = Rule(**validated_request)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@rules_router.put("/rules/{rule_id}")
def update_rule(rule_id: int, request: dict, db: Session = Depends(get_db), _=Depends(get_current_user_from_request)):
    validated_request = validate_rule(request)
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    for key, value in validated_request.items():
        if key not in ["id", "created_at"]:
            setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return rule

@rules_router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db), _=Depends(get_current_user_from_request)):
    db.query(EventLog).filter(EventLog.rule_id == rule_id).delete()
    db.query(Rule).filter(Rule.id == rule_id).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
