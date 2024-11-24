from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Rule
from .auth import get_current_user_from_request
from app.mqtt_client import MQTTClientSingleton

controllers_router = APIRouter()
mqtt_client = MQTTClientSingleton()

@controllers_router.post("/controllers/buzzer")
def set_buzzer_state(request: dict, user=Depends(get_current_user_from_request)):
    frequency = request.get("frequency")
    duration = request.get("duration")
    if not frequency or not duration:
        raise HTTPException(status_code=400, detail="Missing frequency or duration")
    publish_buzzer_state(frequency, duration)
    return {"message": "Buzzer state set"}

@controllers_router.post("/controllers/relay")
def set_relay_state(request: dict, user=Depends(get_current_user_from_request)):
    state = request.get("active")
    if state is None:
        raise HTTPException(status_code=400, detail="Missing active")
    publish_relay_state(state)
    return {"message": "Relay state set"}   

@controllers_router.post("/controllers/led")
def set_led_state(request: dict, user=Depends(get_current_user_from_request)):
    state = request.get("active")
    if state is None:
        raise HTTPException(status_code=400, detail="Missing active")
    publish_led_state(state)
    return {"message": "LED state set"}

@controllers_router.post("/controllers/servo")
def set_servo_state(request: dict, user=Depends(get_current_user_from_request)):
    if "angle" in request:
        angle = request.get("angle")
        publish_servo_angle(angle)
    elif "position" in request:
        position = request.get("position")
        publish_servo_position(position)
    else:
        raise HTTPException(status_code=400, detail="Missing angle or position")
    return {"message": "Servo state set"}

@controllers_router.post("/controllers/fan")
def set_fan_speed(request: dict, user=Depends(get_current_user_from_request)):
    speed = request.get("speed")
    if speed is None:
        raise HTTPException(status_code=400, detail="Missing speed")
    publish_fan_speed(int(speed))
    return {"message": "Fan speed set"}

@controllers_router.post("/controllers/lcd")
def set_lcd_state(request: dict, user=Depends(get_current_user_from_request)):
    message = request.get("message")
    duration = request.get("duration")
    if message is None or duration is None:
        raise HTTPException(status_code=400, detail="Missing message or duration")
    publish_lcd_state(message, duration)
    return {"message": "LCD state set"}

def publish_buzzer_state(frequency: int, duration: int, device_id: str = "esp32_01"):
    if mqtt_client.is_connected():
        mqtt_client.publish(f"farm/{device_id}/buzzer/cmd", {"frequency": frequency, "duration": duration})
    else:
        raise ConnectionError("MQTT client is not connected")

def publish_fan_speed(speed: int, device_id: str = "esp32_01"):
    if mqtt_client.is_connected():
        mqtt_client.publish(f"farm/{device_id}/fan/cmd", {"speed": speed})
    else:
        raise ConnectionError("MQTT client is not connected")
    
def publish_relay_state(state: bool, device_id: str = "esp32_01"):
    if mqtt_client.is_connected():
        mqtt_client.publish(f"farm/{device_id}/relay/cmd", {"active": state})
    else:
        raise ConnectionError("MQTT client is not connected")
    
def publish_led_state(state: bool, device_id: str = "esp32_01"):
    if mqtt_client.is_connected():
        mqtt_client.publish(f"farm/{device_id}/led/cmd", {"active": state})
    else:
        raise ConnectionError("MQTT client is not connected")
    
def publish_servo_angle(angle: int, device_id: str = "esp32_01"):
    if mqtt_client.is_connected():
        mqtt_client.publish(f"farm/{device_id}/servo/cmd", {"angle": angle})
    else:
        raise ConnectionError("MQTT client is not connected")

def publish_servo_position(position: str, device_id: str = "esp32_01"):
    if mqtt_client.is_connected():
        if position not in ["OPEN", "HALF_OPEN", "CLOSED"]:
            raise ValueError("Invalid position")
        mqtt_client.publish(f"farm/{device_id}/servo/cmd", {"position": position})
    else:
        raise ConnectionError("MQTT client is not connected")

def publish_lcd_state(message: str, duration: int, device_id: str = "esp32_01"):
    if mqtt_client.is_connected():
        mqtt_client.publish(f"farm/{device_id}/lcd/cmd", {"message": message, "duration": duration})
    else:
        raise ConnectionError("MQTT client is not connected")
    

