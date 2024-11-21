from app.mqtt_client import start_mqtt_client
from app.routes import app
from app.config import Config
import threading

Config.load_from_args()

if __name__ == "__main__":
    import uvicorn
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
