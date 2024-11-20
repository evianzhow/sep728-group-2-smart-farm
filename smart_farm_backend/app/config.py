import os

class Config:
    MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    DB_URI = os.getenv("DB_URI", "sqlite:///iot_data.db")
