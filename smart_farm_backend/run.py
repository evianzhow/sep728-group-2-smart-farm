from app.mqtt_client import start_mqtt_client
from app.routes import app
from app.config import Config
import threading
import signal
import sys

Config.load_from_args()

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
    
    mqtt_thread = threading.Thread(target=start_mqtt_client, daemon=True)
    mqtt_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
