import os

class Config:
    MQTT_BROKER = os.getenv("MQTT_BROKER", "06a68c084516440da5d6c84b6514ed49.s1.eu.hivemq.cloud")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
    DB_URI = os.getenv("DB_URI", "sqlite:///iot_data.db")
