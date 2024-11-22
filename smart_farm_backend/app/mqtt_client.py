import paho.mqtt.client as paho
from paho import mqtt
import json
import time
from app.models import (
    Steam, Button, Temperature, Humidity, DewPoint, PIR, SoilHumidity,
    WaterLevel, Ultrasonic, Photoresistor, Buzzer, Fan, Relay, LED, Servo, LCD
)
from app.database import SessionLocal
from app.config import Config

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

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


mqtt_client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv31)

def mqtt_publish(topic, payload):
    mqtt_client.publish(topic, json.dumps(payload))

def on_message(client, userdata, message):
    db = SessionLocal()
    try:
        payload = json.loads(message.payload)
        component = message.topic.split("/")[2]
        device_id = message.topic.split("/")[1]

        if component == "dht11":
            # Handle composite DHT11 sensor data
            timestamp = payload.get("timestamp")
            
            # Handle humidity
            if "humidity" in payload:
                humidity_data = {
                    "value": payload["humidity"]["value"],
                    "timestamp": timestamp
                }
                record = COMPONENT_CLASS_MAP["humidity"](**humidity_data, device_id=device_id)
                db.add(record)

            # Handle temperature
            if "temperature" in payload:
                temp_data = {
                    "celsius": payload["temperature"]["celsius"],
                    "fahrenheit": payload["temperature"]["fahrenheit"],
                    "kelvin": payload["temperature"]["kelvin"],
                    "timestamp": timestamp
                }
                record = COMPONENT_CLASS_MAP["temperature"](**temp_data, device_id=device_id)
                db.add(record)

            # Handle dewPoint
            if "dewPoint" in payload:
                dewpoint_data = {
                    "celsius": payload["dewPoint"]["celsius"],
                    "timestamp": timestamp
                }
                record = COMPONENT_CLASS_MAP["dewPoint"](**dewpoint_data, device_id=device_id)
                db.add(record)

            db.commit()
        else:
            # Handle regular single-component sensors
            model_class = COMPONENT_CLASS_MAP.get(component)
            if model_class:
                record = model_class(**payload, device_id=device_id)
                db.add(record)
                db.commit()
            else:
                print(f"Unknown component type: {component}")
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        db.close()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("farm/+/+/state", qos=0)
    client.message_callback_add("farm/+/+/state", on_message)


def start_mqtt_client():
    # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
    # userdata is user defined data of any type, updated by user_data_set()
    # client_id is the given name of the client
    mqtt_client.on_connect = on_connect

    # enable TLS for secure connection
    mqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    mqtt_client.username_pw_set(Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
    mqtt_client.connect(Config.MQTT_BROKER, Config.MQTT_PORT)

    # setting callbacks, use separate functions like above for better visibility
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_message = on_message
    mqtt_client.on_publish = on_publish

    # subscribe to all topics of encyclopedia by using the wildcard "#"
    mqtt_client.subscribe("farm/+/+/state", qos=0)

    # loop_forever for simplicity, here you need to stop the loop manually
    # you can also use loop_start and loop_stop
    while True:  # Reconnect loop for resilience
        try:
            mqtt_client.loop_forever()
        except Exception as e:
            print(f"MQTT client error: {e}")
            time.sleep(5)  # Retry after delay