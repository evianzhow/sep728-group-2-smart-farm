import json
import time
from app.database import SessionLocal
from app.models import Rule
from app.mqtt_client import MQTTClientSingleton

mqtt_client = MQTTClientSingleton()

def evaluate_rules(sensor_data):
    db = SessionLocal()
    rules = db.query(Rule).filter(Rule.trigger_sensor == sensor_data.component).all()

    for rule in rules:
        if eval(f"{sensor_data.value} {rule.op} {rule.threshold}"):
            topic = f"farm/{sensor_data.device_id}/{rule.target_controller}/cmd"
            payload = json.loads(rule.action)  # Store actions as JSON in DB
            mqtt_client.publish(topic, payload)

    db.close()

def check_rules():
    print("Checking rules...")
    pass

def start_rules_engine():
    while True:
        try:
            check_rules()
        except Exception as e:
            print(f"Rule engine error: {e}")
        finally:
            time.sleep(5)  # Wait before restarting the engine
