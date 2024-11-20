from paho.mqtt.client import Client
import json
import time
from app.models import (
    Steam, Button, Temperature, Humidity, DewPoint, PIR, SoilHumidity,
    WaterLevel, Ultrasonic, Photoresistor, Buzzer, Fan, Relay, LED, Servo, LCD
)
from app.database import SessionLocal

COMPONENT_CLASS_MAP = {
    "steam": Steam,
    "button": Button,
    "temperature": Temperature,
    "humidity": Humidity,
    "dewPoint": DewPoint,
    "pir": PIR,
    "soil": SoilHumidity,
    "water": WaterLevel,
    "ultrasonic": Ultrasonic,
    "light": Photoresistor,
    "buzzer": Buzzer,
    "fan": Fan,
    "relay": Relay,
    "led": LED,
    "servo": Servo,
    "lcd": LCD,
}

mqtt_client = Client()

def mqtt_publish(topic, payload):
    mqtt_client.publish(topic, json.dumps(payload))

def on_message(client, userdata, message):
    db = SessionLocal()
    try:
        payload = json.loads(message.payload)
        component = message.topic.split("/")[2]
        model_class = COMPONENT_CLASS_MAP.get(component)

        if model_class:
            record = model_class(**payload, device_id=message.topic.split("/")[1])
            db.add(record)
            db.commit()
        else:
            print(f"Unknown component type: {component}")
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        db.close()

def start_mqtt_client():
    mqtt_client.on_message = on_message
    mqtt_client.connect("broker.hivemq.com", 1883)

    while True:  # Reconnect loop for resilience
        try:
            mqtt_client.loop_forever()
        except Exception as e:
            print(f"MQTT client error: {e}")
            time.sleep(5)  # Retry after delay
