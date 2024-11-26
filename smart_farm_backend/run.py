from app.mqtt_client import MQTTClientSingleton
from app.routes import app
from app.config import Config
from app.rule_engine import start_rules_engine
import threading
import signal
import sys
import time

Config.load_from_args()

def start_mqtt_client():
    mqtt_client = MQTTClientSingleton()
    mqtt_client.connect(Config.MQTT_BROKER, Config.MQTT_PORT, Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
    
    # loop_forever for simplicity, here you need to stop the loop manually
    # you can also use loop_start and loop_stop
    while True:  # Reconnect loop for resilience
        try:
            mqtt_client.loop_forever()
        except Exception as e:
            print(f"MQTT client error: {e}")
            time.sleep(5)  # Retry after delay

def handle_shutdown(signum, frame):
    print("Shutting down gracefully...")
    # Signal the MQTT thread to stop (you'll need to implement this in mqtt_client)
    if mqtt_thread.is_alive():
        mqtt_thread.join(timeout=5)  # Wait up to 5 seconds for MQTT thread to finish
    sys.exit(0)

if __name__ == "__main__":
    import uvicorn
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    # Start MQTT client in a separate thread
    mqtt_thread = threading.Thread(target=start_mqtt_client, daemon=True)
    mqtt_thread.start()

    # Start Rules Engine in a separate thread
    rules_thread = threading.Thread(target=start_rules_engine, daemon=True)
    rules_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=8000)
