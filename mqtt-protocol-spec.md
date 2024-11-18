# MQTT Protocol Specification for ESP32 Toy Farm Kit

## Base Topic Structure
All topics will follow the pattern: `farm/{deviceID}/{component}/{action}`
- `deviceID`: Unique identifier for each ESP32 kit
- `component`: Sensor or controller name
- `action`: Either `state` (for current status) or `cmd` (for commands)

## Device ID

Device ID should be `esp32_01` in this case

## Sensors (Input Devices)

### Button Module
- Type: Sensor
- Value Type: Boolean
- Topic: `farm/{deviceID}/button/state`
- Payload: `{"pressed": true|false}`

### Steam Sensor
- Type: Sensor
- Value Type: Integer
- Range: 0-4095
- Topic: `farm/{deviceID}/steam/state`
- Payload: `{"value": 0-4095, "percentage": 0-100}`

### DHT11 Temperature and Humidity Sensor
- Type: Sensor
- Topic: `farm/{deviceID}/dht11/state`
- According to Datasheet of DHT11, humidity & temperature will be integer value, dew point was calculated with formula, so its type should be float
- Payload:
```json
{
    "humidity": {
        "value": 0-100,
        "unit": "%"
    },
    "temperature": {
        "celsius": 0-50,
        "fahrenheit": 32-122,
        "kelvin": 273.15-323.15
    },
    "dewPoint": {
        "celsius": 0-50
    }
}
```

### PIR Motion Sensor
- Type: Sensor
- Value Type: Boolean
- Topic: `farm/{deviceID}/pir/state`
- Event will be trigger when the state flips (not detected -> detected and vice versa)
- Payload: `{"motion_detected": true|false}`

### Soil Humidity Sensor
- Type: Sensor
- Value Type: Integer
- Range: 0-4095
- Topic: `farm/{deviceID}/soil/state`
- Payload: `{"raw": 0-4095, "percentage": 0-100}`

### Water Level Sensor
- Type: Sensor
- Value Type: Integer
- Range: 0-4095
- Topic: `farm/{deviceID}/water/state`
- Payload: `{"raw": 0-4095, "percentage": 0-100}`

### SR01 V3 Ultrasonic Module
- Type: Sensor
- Value Type: Float
- Range: 3-8 cm
- Topic: `farm/{deviceID}/ultrasonic/state`
- Payload: `{"distance": 3-8, "unit": "cm"}`

### Photoresistor
- Type: Sensor
- Value Type: Integer
- Range: >0
- Topic: `farm/{deviceID}/light/state`
- Payload: `{"value": >0, "percentage": 0-100}`

## Controllers (Output Devices)

### Passive Buzzer
- Type: Controller
- Topics:
  - Status: `farm/{deviceID}/buzzer/state`
  - Control: `farm/{deviceID}/buzzer/cmd`
- `duration` is in milliseconds
- Payload:
```json
{
    "active": true|false,
    "frequency": 0-20000,
    "duration": 0-65535
}
```

### 130 Motor (Fan)
- Type: Controller
- Topics:
  - Status: `farm/{deviceID}/fan/state`
  - Control: `farm/{deviceID}/fan/cmd`
- `0` stands for stop the fan, `255` will be the maximum speed
- Payload: `{"speed": 0-255}`

### 5V Relay Module
- Type: Controller
- Topics:
  - Status: `farm/{deviceID}/relay/state`
  - Control: `farm/{deviceID}/relay/cmd`
- Payload: `{"active": true|false}`

### White LED Module
- Type: Controller
- Topics:
  - Status: `farm/{deviceID}/led/state`
  - Control: `farm/{deviceID}/led/cmd`
- Payload: `{"active": true|false}`

### Servo
- Type: Controller
- Topics:
  - Status: `farm/{deviceID}/servo/state`
  - Control: `farm/{deviceID}/servo/cmd`
  - Preset Angles: 
    - OPEN: 80
    - HALF_OPEN: 120
    - CLOSED: 180
- Either `angle` or `position` will work but `angle` has first priority
- Payload:
```json
{
    "angle": 0-180,
    "position": "OPEN|HALF_OPEN|CLOSED"
}
```

### LCD
- Type: Controller
- Topics:
  - Status: `farm/{deviceID}/lcd/state`
  - Control: `farm/{deviceID}/lcd/cmd`
- `duration` is in milliseconds
- Payload:
```json
{
    "message": "Hello World!",
    "duration": 10000
}
```

## Example Usage

### Publishing sensor data:
```
Topic: farm/esp32_01/dht11/state
Payload: {"humidity":{"value":45.2,"unit":"%"},"temperature":{"celsius":24.5,"fahrenheit":76.1,"kelvin":297.65},"dewPoint":{"celsius":12.3}}
```

### Controlling a device:
```
Topic: farm/esp32_01/servo/cmd
Payload: {"position":"HALF_OPEN"}
```

### Error Handling
All devices should publish errors to: `farm/{deviceID}/error`
Payload format:
```json
{
    "component": "component_name",
    "error_code": "ERROR_CODE",
    "message": "Error description",
    "timestamp": "ISO8601_TIMESTAMP"
}
```
