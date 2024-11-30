import json
import time
from app.database import SessionLocal
from app.models import Rule
from app.mqtt_client import MQTTClientSingleton, COMPONENT_CLASS_MAP
from app.models import SensorDataBase, EventLog
from app.routes.controllers import publish_buzzer_state, publish_fan_speed, publish_relay_state, publish_led_state, publish_lcd_state, publish_servo_position

mqtt_client = MQTTClientSingleton()

def check_rules():
    db = SessionLocal()
    rules = db.query(Rule).all()
    for rule in rules:
        # Get the table name of the trigger sensor
        trigger_sensor = rule.trigger_sensor.split(".")[0]
        if trigger_sensor == "dht11":
            component = rule.trigger_sensor.split(".")[1]
            if component == "humidity":
                matched_record = traverse_db_and_find_first_matched_record(db, "humidity", rule)
                if matched_record and not check_record_already_triggered(db, rule, matched_record):
                    trigger_rule(rule)
                    mark_record_as_triggered(db, rule, matched_record)
            elif component == "temperature":
                matched_record = traverse_db_and_find_first_matched_record(db, "temperature", rule)
                if matched_record and not check_record_already_triggered(db, rule, matched_record):
                    trigger_rule(rule)
                    mark_record_as_triggered(db, rule, matched_record)
            elif component == "dewpoint":
                matched_record = traverse_db_and_find_first_matched_record(db, "dewPoint", rule)
                if matched_record and not check_record_already_triggered(db, rule, matched_record):
                    trigger_rule(rule)
                    mark_record_as_triggered(db, rule, matched_record)
            else:
                raise Exception(f"Invalid trigger sensor: {rule.trigger_sensor}")
        else:
            matched_record = traverse_db_and_find_first_matched_record(db, trigger_sensor, rule)
            if matched_record and not check_record_already_triggered(db, rule, matched_record):
                trigger_rule(rule)
                mark_record_as_triggered(db, rule, matched_record)
    db.close()

def traverse_db_and_find_first_matched_record(db, model_class_name: str, rule: Rule):
    # print(f"Traversing DB for model class {model_class_name} and rule {rule.id}")
    model_class = COMPONENT_CLASS_MAP[model_class_name]
    queries = db.query(model_class).order_by(model_class.timestamp.desc()).limit(100) # We only need the latest 100 records
    # return the first match meeting the rule
    for query in queries:
        match model_class_name:
            case "humidity":
                if eval(f"{query.value} {rule.op} {rule.threshold}"):
                    return query
            case "temperature":
                unit = rule.trigger_sensor.split(".")[2]
                if unit == "celsius":
                    if eval(f"{query.celsius} {rule.op} {rule.threshold}"):
                        return query
                elif unit == "fahrenheit":
                    if eval(f"{query.fahrenheit} {rule.op} {rule.threshold}"):
                        return query
                elif unit == "kelvin":
                    if eval(f"{query.kelvin} {rule.op} {rule.threshold}"):
                        return query
            case "dewPoint":
                unit = rule.trigger_sensor.split(".")[2]
                if unit == "celsius":
                    if eval(f"{query.celsius} {rule.op} {rule.threshold}"):
                        return query
            case "button":
                if query.pressed == (rule.op == "pressed"):
                    return query
            case "pir":
                if query.motion_detected == (rule.op == "detected"):
                    return query
            case "relay":
                if query.active == (rule.op == "active"):
                    return query
            case "led":
                if query.active == (rule.op == "active"):
                    return query
            case "servo":
                if query.position == rule.op:
                    return query
            case _:
                column_name = rule.trigger_sensor.split(".")[1]
                if eval(f"{getattr(query, column_name)} {rule.op} {rule.threshold}"):
                    return query

def check_record_already_triggered(db, rule: Rule, record: SensorDataBase):
    # print(f"Checking if record {record.id} for rule {rule.id} has already been triggered")
    return db.query(EventLog).filter(EventLog.rule_id == rule.id, EventLog.triggered_record_id == record.id).first() is not None

def mark_record_as_triggered(db, rule: Rule, record: SensorDataBase):
    print(f"Marking record {record.id} for rule {rule.id} as triggered")
    event_log = EventLog(rule_id=rule.id, triggered_record_id=record.id)
    db.add(event_log)
    db.commit()

def trigger_rule(rule: Rule):
    print(f"Triggering rule {rule.id}")
    target_controller = rule.target_controller
    action_arr = rule.action.split(";")
    action_dict = {kv.split("=")[0]: kv.split("=")[1] for kv in action_arr}

    match target_controller:
        case "buzzer":
            publish_buzzer_state(int(action_dict["frequency"]), int(action_dict["duration"]))
        case "fan":
            publish_fan_speed(int(action_dict["speed"]))
        case "relay":
            publish_relay_state(action_dict["active"] == "true")
        case "lcd":
            publish_lcd_state(action_dict["message"], int(action_dict["duration"]))
        case "servo":
            # We stored the action in lowercase in the DB
            publish_servo_position(action_dict["position"].upper())
        case "led":
            publish_led_state(action_dict["active"] == "true")

def start_rules_engine():
    while True:
        try:
            check_rules()
        except Exception as e:
            print(f"Rule engine error: {e}")
        finally:
            time.sleep(1)  # Wait before restarting the engine
