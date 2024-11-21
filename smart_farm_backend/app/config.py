import os
import argparse
from typing import Optional

class Config:
    MQTT_BROKER = os.getenv("MQTT_BROKER", "06a68c084516440da5d6c84b6514ed49.s1.eu.hivemq.cloud")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None
    DB_URI = os.getenv("DB_URI", "sqlite:///iot_data.db")

    @classmethod
    def load_from_args(cls) -> None:
        """Load configuration from command line arguments"""
        parser = argparse.ArgumentParser(description='MQTT Client Configuration')
        parser.add_argument('--mqtt-broker', help='MQTT broker address')
        parser.add_argument('--mqtt-port', type=int, help='MQTT broker port')
        parser.add_argument('--mqtt-username', help='MQTT username')
        parser.add_argument('--mqtt-password', help='MQTT password')
        parser.add_argument('--config', help='Path to YAML configuration file')
        
        args = parser.parse_args()
        
        # Load from config file first if specified
        if args.config:
            cls.load_from_yaml(args.config)
        
        # Command line arguments override config file
        if args.mqtt_broker:
            cls.MQTT_BROKER = args.mqtt_broker
        if args.mqtt_port:
            cls.MQTT_PORT = args.mqtt_port
        if args.mqtt_username:
            cls.MQTT_USERNAME = args.mqtt_username
        if args.mqtt_password:
            cls.MQTT_PASSWORD = args.mqtt_password