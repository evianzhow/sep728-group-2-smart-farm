from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Steam, Photoresistor, Temperature, Humidity, DewPoint, PIR, SoilHumidity, WaterLevel, Ultrasonic, Button, Buzzer, Fan, Relay, LED, Servo, LCD
from .auth import get_current_user_from_request
from app.utils import convert_datetime_to_iso8601

sensors_router = APIRouter()

@sensors_router.get("/sensors/light/preview")
def get_light_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    light = db.query(Photoresistor).order_by(Photoresistor.timestamp.desc()).first()
    if light is not None:
        light.timestamp = convert_datetime_to_iso8601(light.timestamp)
    return light

@sensors_router.get("/sensors/water/preview")
def get_water_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    water = db.query(WaterLevel).order_by(WaterLevel.timestamp.desc()).first()
    if water is not None:
        water.timestamp = convert_datetime_to_iso8601(water.timestamp)
    return water

@sensors_router.get("/sensors/steam/preview")
def get_steam_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    steam = db.query(Steam).order_by(Steam.timestamp.desc()).first()
    if steam is not None:
        steam.timestamp = convert_datetime_to_iso8601(steam.timestamp)
    return steam

@sensors_router.get("/sensors/button/preview")
def get_button_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    button = db.query(Button).order_by(Button.timestamp.desc()).first()
    if button is not None:
        button.timestamp = convert_datetime_to_iso8601(button.timestamp)
    return button

@sensors_router.get("/sensors/ultrasonic/preview")
def get_ultrasonic_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    ultrasonic = db.query(Ultrasonic).order_by(Ultrasonic.timestamp.desc()).first()
    if ultrasonic is not None:
        ultrasonic.timestamp = convert_datetime_to_iso8601(ultrasonic.timestamp)
    return ultrasonic

@sensors_router.get("/sensors/dht11/temperature/preview")
def get_dht11_temperature_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    temperature = db.query(Temperature).order_by(Temperature.timestamp.desc()).first()
    if temperature is not None:
        return {
            "temperature": {
                "celsius": temperature.celsius,
                "fahrenheit": temperature.fahrenheit,
                "kelvin": temperature.kelvin
            },
            "timestamp": convert_datetime_to_iso8601(temperature.timestamp)
        }
    else:
        return None

@sensors_router.get("/sensors/dht11/humidity/preview")
def get_dht11_humidity_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    humidity = db.query(Humidity).order_by(Humidity.timestamp.desc()).first()
    if humidity is not None:
        return {
            "humidity": {
                "value": humidity.value,
                "unit": humidity.unit
            },
            "timestamp": convert_datetime_to_iso8601(humidity.timestamp)
        }
    else:
        return None

@sensors_router.get("/sensors/dht11/dewpoint/preview")
def get_dht11_dewpoint_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    dewpoint = db.query(DewPoint).order_by(DewPoint.timestamp.desc()).first()
    if dewpoint is not None:
        return {
            "dewpoint": {
                "celsius": dewpoint.celsius
            },
            "timestamp": convert_datetime_to_iso8601(dewpoint.timestamp)
        }
    else:
        return None

@sensors_router.get("/sensors/pir/preview")
def get_pir_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    pir = db.query(PIR).order_by(PIR.timestamp.desc()).first()
    if pir is not None:
        return {
            "value": pir.motion_detected,
            "timestamp": convert_datetime_to_iso8601(pir.timestamp)
        }
    else:
        return None

@sensors_router.get("/sensors/soil/preview")
def get_soil_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    soil = db.query(SoilHumidity).order_by(SoilHumidity.timestamp.desc()).first()
    if soil is not None:
        soil.timestamp = convert_datetime_to_iso8601(soil.timestamp)
    return soil

# Controllers   
@sensors_router.get("/controllers/buzzer/preview")
def get_buzzer_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    buzzer = db.query(Buzzer).order_by(Buzzer.timestamp.desc()).first()
    if buzzer is not None:
        buzzer.timestamp = convert_datetime_to_iso8601(buzzer.timestamp)
    return buzzer

@sensors_router.get("/controllers/fan/preview")
def get_fan_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    fan = db.query(Fan).order_by(Fan.timestamp.desc()).first()
    if fan is not None:
        fan.timestamp = convert_datetime_to_iso8601(fan.timestamp)
    return fan

@sensors_router.get("/controllers/relay/preview")
def get_relay_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    relay = db.query(Relay).order_by(Relay.timestamp.desc()).first()
    if relay is not None:
        relay.timestamp = convert_datetime_to_iso8601(relay.timestamp)
    return relay

@sensors_router.get("/controllers/led/preview")
def get_led_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    led = db.query(LED).order_by(LED.timestamp.desc()).first()
    if led is not None:
        led.timestamp = convert_datetime_to_iso8601(led.timestamp)
    return led

@sensors_router.get("/controllers/servo/preview")
def get_servo_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    servo = db.query(Servo).order_by(Servo.timestamp.desc()).first()
    if servo is not None:
        servo.timestamp = convert_datetime_to_iso8601(servo.timestamp)
    return servo

@sensors_router.get("/controllers/lcd/preview")
def get_lcd_preview(user=Depends(get_current_user_from_request)):
    db = SessionLocal()
    lcd = db.query(LCD).order_by(LCD.timestamp.desc()).first()
    if lcd is not None:
        lcd.timestamp = convert_datetime_to_iso8601(lcd.timestamp)
    return lcd

