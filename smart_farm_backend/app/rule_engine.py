import json
from app.database import SessionLocal
from app.models import Rule
from app.mqtt_client import mqtt_publish

def evaluate_rules(sensor_data):
    db = SessionLocal()
    rules = db.query(Rule).filter(Rule.trigger_sensor == sensor_data.component).all()

    for rule in rules:
        if eval(f"{sensor_data.value} {rule.op} {rule.threshold}"):
            topic = f"farm/{sensor_data.device_id}/{rule.target_controller}/cmd"
            payload = json.loads(rule.action)  # Store actions as JSON in DB
            mqtt_publish(topic, payload)

    db.close()
