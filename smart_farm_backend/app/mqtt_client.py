import paho.mqtt.client as paho
from paho import mqtt
import json
import time
from app.models import (
    Steam, Button, Temperature, Humidity, DewPoint, PIR, SoilHumidity,
    WaterLevel, Ultrasonic, Photoresistor, Buzzer, Fan, Relay, LED, Servo, LCD
)
from app.database import SessionLocal
import threading

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

class MQTTClientSingleton:
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    _is_connected = False  # Track connection status

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv31)
            # Update connection status in callback
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_publish = self._on_publish
            self.client.on_subscribe = self._on_subscribe

            self._initialized = True

    def connect(self, broker: str, port: int, username: str, password: str, tls: bool = True):
        if tls:
            self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password)
        self.client.connect(broker, port)

    def _on_connect(self, client, userdata, flags, rc):
        self._is_connected = rc == 0
        print(f"Connected with result code {rc}")
        self.client.subscribe("farm/+/+/state", qos=0)
        self.client.message_callback_add("farm/+/+/state", self._on_message)

    def _on_disconnect(self, client, userdata, rc):
        self._is_connected = False
        print(f"Disconnected with result code {rc}")

    def _on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print(f"Subscribed: {mid} {granted_qos}")

    def is_connected(self) -> bool:
        return self._is_connected and self.client.is_connected()

    def publish(self, topic, payload, qos=0):
        if not self.is_connected():
            raise ConnectionError("MQTT client is not connected")
        self.client.publish(topic, json.dumps(payload), qos=qos)

    def get_client(self):
        return self.client

    def _on_publish(self, client, userdata, mid):
        print(f"Published message with mid: {mid}")

    def _on_message(self, client, userdata, message):
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

    def loop_forever(self):
        self.client.loop_forever()
