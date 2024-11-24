from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declared_attr
from app.database import Base

class SensorDataBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    component = Column(String, index=True)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        if 'timestamp' in kwargs and isinstance(kwargs['timestamp'], str):
            kwargs['timestamp'] = datetime.fromisoformat(kwargs['timestamp'].replace('Z', '+00:00'))
        super().__init__(**kwargs)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class Steam(SensorDataBase):
    value = Column(Integer)  # Raw sensor reading
    percentage = Column(Float)

class Button(SensorDataBase):
    pressed = Column(Boolean)

class Temperature(SensorDataBase):
    celsius = Column(Float)
    fahrenheit = Column(Float)
    kelvin = Column(Float)

class Humidity(SensorDataBase):
    value = Column(Float)
    unit = Column(String, default="%")

class DewPoint(SensorDataBase):
    celsius = Column(Float)

class PIR(SensorDataBase):
    motion_detected = Column(Boolean)

class SoilHumidity(SensorDataBase):
    value = Column(Integer)
    percentage = Column(Float)

class WaterLevel(SensorDataBase):
    value = Column(Integer)
    percentage = Column(Float)

class Ultrasonic(SensorDataBase):
    value = Column(Float)
    unit = Column(String, default="cm")

class Photoresistor(SensorDataBase):
    value = Column(Integer)
    percentage = Column(Float)

# Controllers
class Buzzer(SensorDataBase):
    active = Column(Boolean)
    frequency = Column(Integer)
    duration = Column(Integer)

class Fan(SensorDataBase):
    speed = Column(Integer)

class Relay(SensorDataBase):
    active = Column(Boolean)

class LED(SensorDataBase):
    active = Column(Boolean)

class Servo(SensorDataBase):
    angle = Column(Integer)
    position = Column(String)

class LCD(SensorDataBase):
    message = Column(String)
    duration = Column(Integer)

class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    trigger_sensor = Column(String, nullable=False)
    op = Column(String, nullable=False)  # e.g., '>', '<=', etc.
    threshold = Column(Float, nullable=True)
    target_controller = Column(String, nullable=False)
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)  # Store hashed password
