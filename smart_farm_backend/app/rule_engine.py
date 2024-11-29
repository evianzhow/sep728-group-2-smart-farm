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
    db = SessionLocal()
    try:
        rules = db.query(Rule).all()
        for rule in rules:
            # Get latest sensor data for the trigger sensor
            sensor_data = db.query(SensorData)\
                .filter(SensorData.component == rule.trigger_sensor)\
                .order_by(SensorData.timestamp.desc())\
                .first()
            
            if sensor_data:
                # Evaluate rule condition
                if eval(f"{sensor_data.value} {rule.op} {rule.threshold}"):
                    # Use controller methods to publish based on target controller
                    action = json.loads(rule.action)
                    if rule.target_controller == "buzzer":
                        publish_buzzer_state(action["frequency"], action["duration"], sensor_data.device_id)
                    elif rule.target_controller == "fan":
                        publish_fan_speed(action["speed"], sensor_data.device_id)
                    elif rule.target_controller == "relay":
                        publish_relay_state(action["active"], sensor_data.device_id)
                    elif rule.target_controller == "led":
                        publish_led_state(action["active"], sensor_data.device_id)
                    elif rule.target_controller == "servo":
                        if "angle" in action:
                            publish_servo_angle(action["angle"], sensor_data.device_id)
                        elif "position" in action:
                            publish_servo_position(action["position"], sensor_data.device_id)
                    elif rule.target_controller == "lcd":
                        publish_lcd_state(action["message"], action["duration"], sensor_data.device_id)
                    
    finally:
        db.close()

    
    pass

def start_rules_engine():
    while True:
        try:
            check_rules()
        except Exception as e:
            print(f"Rule engine error: {e}")
        finally:
            time.sleep(5)  # Wait before restarting the engine
