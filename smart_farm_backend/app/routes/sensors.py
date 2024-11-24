from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Steam, Photoresistor, Temperature, Humidity, DewPoint, PIR, SoilHumidity, WaterLevel, Ultrasonic, Button, Buzzer, Fan, Relay, LED, Servo, LCD
from .auth import get_current_user_from_request

sensors_router = APIRouter()

@sensors_router.get("/sensors/light/preview")
def get_light_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    light = db.query(Photoresistor).order_by(Photoresistor.timestamp.desc()).first()
    return light

@sensors_router.get("/sensors/water/preview")
def get_water_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    water = db.query(WaterLevel).order_by(WaterLevel.timestamp.desc()).first()
    return water

@sensors_router.get("/sensors/steam/preview")
def get_steam_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    steam = db.query(Steam).order_by(Steam.timestamp.desc()).first()
    return steam

@sensors_router.get("/sensors/button/preview")
def get_button_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    button = db.query(Button).order_by(Button.timestamp.desc()).first()
    return button

@sensors_router.get("/sensors/ultrasonic/preview")
def get_ultrasonic_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    ultrasonic = db.query(Ultrasonic).order_by(Ultrasonic.timestamp.desc()).first()
    return ultrasonic

@sensors_router.get("/sensors/dht11/temperature/preview")
def get_dht11_temperature_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    temperature = db.query(Temperature).order_by(Temperature.timestamp.desc()).first()
    return {
        "temperature": {
            "celsius": temperature.celsius,
            "fahrenheit": temperature.fahrenheit,
            "kelvin": temperature.kelvin
        },
        "timestamp": temperature.timestamp
    }

@sensors_router.get("/sensors/dht11/humidity/preview")
def get_dht11_humidity_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    humidity = db.query(Humidity).order_by(Humidity.timestamp.desc()).first()
    return {
        "humidity": {
            "value": humidity.value,
            "unit": humidity.unit
        },
        "timestamp": humidity.timestamp
    } 

@sensors_router.get("/sensors/dht11/dewpoint/preview")
def get_dht11_dewpoint_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    dewpoint = db.query(DewPoint).order_by(DewPoint.timestamp.desc()).first()
    return {
        "dewpoint": {
            "celsius": dewpoint.celsius
        },
        "timestamp": dewpoint.timestamp
    }

@sensors_router.get("/sensors/pir/preview")
def get_pir_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    pir = db.query(PIR).order_by(PIR.timestamp.desc()).first()
    return {
        "value": pir.motion_detected,
        "timestamp": pir.timestamp
    }

@sensors_router.get("/sensors/soil/preview")
def get_soil_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    soil = db.query(SoilHumidity).order_by(SoilHumidity.timestamp.desc()).first()
    return soil

# Controllers   
@sensors_router.get("/controllers/buzzer/preview")
def get_buzzer_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    buzzer = db.query(Buzzer).order_by(Buzzer.timestamp.desc()).first()
    return buzzer

@sensors_router.get("/controllers/fan/preview")
def get_fan_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    fan = db.query(Fan).order_by(Fan.timestamp.desc()).first()
    return fan

@sensors_router.get("/controllers/relay/preview")
def get_relay_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    relay = db.query(Relay).order_by(Relay.timestamp.desc()).first()
    return relay

@sensors_router.get("/controllers/led/preview")
def get_led_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    led = db.query(LED).order_by(LED.timestamp.desc()).first()
    return led

@sensors_router.get("/controllers/servo/preview")
def get_servo_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    servo = db.query(Servo).order_by(Servo.timestamp.desc()).first()
    return servo

@sensors_router.get("/controllers/lcd/preview")
def get_lcd_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    lcd = db.query(LCD).order_by(LCD.timestamp.desc()).first()
    return lcd

