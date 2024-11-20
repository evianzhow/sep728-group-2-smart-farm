from app.mqtt_client import start_mqtt_client
from app.routes import app

if __name__ == "__main__":
    import uvicorn
    start_mqtt_client()
    uvicorn.run(app, host="0.0.0.0", port=8000)
