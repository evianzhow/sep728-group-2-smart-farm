# Smart Farm System API Documentation

## Base URL
```
https://gorgeous-glowworm-definite.ngrok-free.app
```

## Authentication
All API endpoints require authentication token except for login.

Authentication token is sent in the header of each request.

### Headers
```
Authorization: <token>
```

## Authentication Endpoints

### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "token": "string",
}
```

### Logout
```http
POST /auth/logout
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

## Sensor Endpoints

### Light Sensor

#### Get Latest Light Reading
```http
GET /sensors/light/preview
```

**Response (200 OK):**
```json
{
  "value": 2663,
  "percentage": 65,
  "timestamp": "2024-11-20T11:18:17.000Z"
}
```

#### Get Light History
```http
GET /sensors/light/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "value": 2663,
      "percentage": 65,
      "timestamp": "2024-11-20T11:18:17.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

#### Get Light Chart Data
```http
GET /sensors/light/chart
```

**Query Parameters:**
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string
- `interval`: string (optional, default: "hour", enum: ["minute", "hour", "day"]), when using preview, interval must be "minute"

**Response (200 OK):**
```json
{
  "data": [
    { // Data will be aggregated and calculated of mean by interval
      "timestamp": 1700480400000,  // Unix timestamp in milliseconds
      "value": 2663,
      "percentage": 65
    }
  ],
  "metadata": {
    "start_time": 1700480400000,
    "end_time": 1700484000000,
    "interval": "hour",
  }
}
```

### Water Sensor

#### Get Latest Water Reading
```http
GET /sensors/water/preview
```

**Response (200 OK):**
```json
{
  "value": 0,
  "percentage": 0,
  "timestamp": "2024-11-20T11:18:17.000Z"
}
``` 

#### Get Water History
```http
GET /sensors/water/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "value": 0,
      "percentage": 0,
      "timestamp": "2024-11-20T11:18:17.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

#### Get Water Chart Data
```http
GET /sensors/water/chart
```

**Query Parameters:**
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string
- `interval`: string (optional, default: "hour", enum: ["minute", "hour", "day"])

**Response (200 OK):**
```json
{
  "data": [
    {
      "timestamp": 1700480400000,  // Unix timestamp in milliseconds
      "value": 0,
      "percentage": 0
    }
  ],
  "metadata": {
    "start_time": 1700480400000,
    "end_time": 1700484000000,
    "interval": "hour",
  }
}
```

### Steam Sensor

#### Get Latest Steam Reading
```http
GET /sensors/steam/preview
```

**Response (200 OK):**
```json
{
  "value": 0,
  "percentage": 0,
  "timestamp": "2024-11-20T11:18:17.000Z"
}
```

#### Get Steam History
```http
GET /sensors/steam/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string


**Response (200 OK):**
```json
{
  "data": [
    {
      "value": 0,
      "percentage": 0,
      "timestamp": "2024-11-20T11:18:17.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

#### Get Steam Chart Data
```http
GET /sensors/steam/chart
```

**Query Parameters:**
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string
- `interval`: string (optional, default: "hour", enum: ["minute", "hour", "day"])

**Response (200 OK):**
```json
{
  "data": [
    {
      "timestamp": 1700480400000,  // Unix timestamp in milliseconds
      "value": 0,
      "percentage": 0
    }
  ],
  "metadata": {
    "start_time": 1700480400000,
    "end_time": 1700484000000,
    "interval": "hour",
  }
}
```

### Ultrasonic Sensor

#### Get Latest Ultrasonic Reading
```http
GET /sensors/ultrasonic/preview
```

**Response (200 OK):**
```json
{
  "value": 8,
  "unit": "cm",
  "timestamp": "2024-11-20T11:18:17.000Z"
}
```

#### Get Ultrasonic History
```http
GET /sensors/ultrasonic/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "value": 8,
      "unit": "cm",
      "timestamp": "2024-11-20T11:18:17.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

#### Get Ultrasonic Chart Data
```http
GET /sensors/ultrasonic/chart
```

**Query Parameters:**
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string
- `interval`: string (optional, default: "hour", enum: ["minute", "hour", "day"])

**Response (200 OK):**
```json
{
  "data": [
    {
      "timestamp": 1700480400000,  // Unix timestamp in milliseconds
      "value": 8,
      "unit": "cm"
    }
  ],
  "metadata": {
    "start_time": 1700480400000,
    "end_time": 1700484000000,
    "interval": "hour",
  }
}
```

### DHT11 Sensor

#### Get Temperature Preview
```http
GET /sensors/dht11/temperature/preview
```

**Response (200 OK):**
```json
{
  "temperature": {
    "celsius": 25,
    "fahrenheit": 77,
    "kelvin": 298.15
  },
  "timestamp": "2024-11-20T11:49:30.000Z"
}
```

#### Get Temperature History
```http
GET /sensors/dht11/temperature/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string
- `unit`: string (optional, default: "celsius", enum: ["celsius", "fahrenheit", "kelvin"])

**Response (200 OK):**
```json
{
  "data": [
    {
      "temperature": {
        "celsius": 25,
        "fahrenheit": 77,
        "kelvin": 298.15
      },
      "timestamp": "2024-11-20T11:49:30.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

#### Get Temperature Chart Data
```http
GET /sensors/dht11/temperature/chart
```

**Query Parameters:**
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string
- `interval`: string (optional, default: "hour", enum: ["minute", "hour", "day"])
- `unit`: string (optional, default: "celsius", enum: ["celsius", "fahrenheit", "kelvin"])

**Response (200 OK):**
```json
{
  "data": [
    {
      "timestamp": 1700480400000,  // Unix timestamp in milliseconds
      "value": 25,
      "unit": "celsius"
    }
  ],
  "metadata": {
    "start_time": 1700480400000,
    "end_time": 1700484000000,
    "interval": "hour",
    "unit": "celsius"
  }
}
```

#### Get Humidity Preview
```http
GET /sensors/dht11/humidity/preview
```

**Response (200 OK):**
```json
{
  "humidity": {
    "value": 36,
    "unit": "%"
  },
  "timestamp": "2024-11-20T11:49:30.000Z"
}
``` 

#### Get Humidity History
```http
GET /sensors/dht11/humidity/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "humidity": {
        "value": 36,
        "unit": "%"
      },
      "timestamp": "2024-11-20T11:49:30.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

#### Get Humidity Chart Data
```http
GET /sensors/dht11/humidity/chart
```

**Query Parameters:**
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string
- `interval`: string (optional, default: "hour", enum: ["minute", "hour", "day"])

**Response (200 OK):**
```json
{
  "data": [
    {
      "timestamp": 1700480400000,  // Unix timestamp in milliseconds
      "value": 36,
      "unit": "%"
    }
  ],
  "metadata": {
    "start_time": 1700480400000,
    "end_time": 1700484000000,
    "interval": "hour",
  }
}
```

#### Get Dew Point Preview
```http
GET /sensors/dht11/dewpoint/preview
```

**Response (200 OK):**
```json
{
  "dewpoint": {
    "celsius": 8.913886708
  },
  "timestamp": "2024-11-20T11:49:30.000Z"
}
```

#### Get Dew Point History
```http
GET /sensors/dht11/dewpoint/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "dewPoint": {
        "celsius": 8.913886708
      },
      "timestamp": "2024-11-20T11:49:30.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

#### Get Dew Point Chart Data
```http
GET /sensors/dht11/dewpoint/chart
```

**Query Parameters:**
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string
- `interval`: string (optional, default: "hour", enum: ["minute", "hour", "day"])
- `unit`: string (optional, default: "celsius", enum: ["celsius"])

**Response (200 OK):**
```json
{
  "data": [
    {
      "timestamp": 1700480400000,  // Unix timestamp in milliseconds
      "value": 8.913886708,
      "unit": "celsius"
    }
  ],
  "metadata": {
    "start_time": 1700480400000,
    "end_time": 1700484000000,
    "interval": "hour",
  }
}
```

### Soil Moisture Sensor

#### Get Latest Soil Moisture Reading
```http
GET /sensors/soil/preview
```

**Response (200 OK):**
```json
{
  "value": 2663,
  "percentage": 65,
  "timestamp": "2024-11-20T11:18:17.000Z"
}
```

#### Get Soil Moisture History
```http
GET /sensors/soil/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "value": 0,
      "percentage": 0,
      "timestamp": "2024-11-20T11:18:17.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

#### Get Soil Moisture Chart Data
```http
GET /sensors/soil/chart
```

**Query Parameters:**
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string
- `interval`: string (optional, default: "hour", enum: ["minute", "hour", "day"])

**Response (200 OK):**
```json
{
  "data": [
    {
      "timestamp": 1700480400000,  // Unix timestamp in milliseconds
      "value": 0,
      "percentage": 0
    }
  ],
  "metadata": {
    "start_time": 1700480400000,
    "end_time": 1700484000000,
    "interval": "hour",
  }
}
```

### PIR Sensor

#### Get Latest PIR Reading
```http
GET /sensors/pir/preview
```

**Response (200 OK):**
```json
{
  "value": true,
  "timestamp": "2024-11-20T11:18:17.000Z"
}
```

#### Get PIR History
```http
GET /sensors/pir/history
```

**Query Parameters:**
- `page`: integer (default: 1) 
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "value": true,
      "timestamp": "2024-11-20T11:18:17.000Z"
    },
    {
      "value": false,
      "timestamp": "2024-11-20T11:18:17.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

### Button

#### Get Latest Button Reading
```http
GET /sensors/button/preview
```

**Response (200 OK):**
```json
{
  "pressed": true,
  "timestamp": "2024-11-20T11:18:17.000Z"
}
```

#### Get Button History
```http
GET /sensors/button/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "pressed": true,
      "timestamp": "2024-11-20T11:18:17.000Z"
    },
    {
      "pressed": false,
      "timestamp": "2024-11-20T11:18:17.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

## Controller Endpoints

### Buzzer Controller

#### Get Latest Buzzer State
```http
GET /controllers/buzzer/preview
```

**Response (200 OK):**
```json
{
  "active": true,
  "frequency": 6000,
  "duration": 1000,
  "timestamp": "2024-11-20T11:57:28.000Z"
}
```

#### Set Buzzer State
```http
POST /controllers/buzzer
```

**Request Body:**
```json
{
  "frequency": 6000,
  "duration": 1000
}
```

**Response (200 OK):**
```json
{
  "error": false,
  "error_message": null
}
```

#### Get Buzzer History
```http
GET /controllers/buzzer/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "active": true,
      "frequency": 6000,
      "duration": 1000,
      "timestamp": "2024-11-20T11:57:28.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

### Relay Controller

#### Get Latest Relay State
```http
GET /controllers/relay/preview
```

**Response (200 OK):**
```json
{
  "active": true,
  "timestamp": "2024-11-20T11:57:51.000Z"
}
```

#### Set Relay State
```http
POST /controllers/relay
```

**Request Body:**
```json
{
  "active": true
}
```

**Response (200 OK):**
```json
{
  "error": false,
  "error_message": null
}
```

#### Get Relay History
```http
GET /controllers/relay/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "active": true,
      "timestamp": "2024-11-20T11:57:51.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

### LED Controller

#### Get Latest LED State
```http
GET /controllers/led/preview
```

**Response (200 OK):**
```json
{
  "active": true,
  "timestamp": "2024-11-20T11:58:13.000Z"
}
```

#### Set LED State
```http
POST /controllers/led
```

**Request Body:**
```json
{
  "active": true
}
```

**Response (200 OK):**
```json
{
  "error": false,
  "error_message": null
}
```

#### Get LED History
```http
GET /controllers/led/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "active": true,
      "timestamp": "2024-11-20T11:58:13.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

### Servo Controller

#### Get Latest Servo State
```http
GET /controllers/servo/preview
```

**Response (200 OK):**
```json
{
  "position": "OPEN",
  "timestamp": "2024-11-20T11:58:42.000Z"
}
```

#### Set Servo State
```http
POST /controllers/servo
```

**Request Body:**
```json
{
  "position": "OPEN"
}
```
**or**
```json
{
  "angle": 90
}
```

**Response (200 OK):**
```json
{
  "error": false,
  "error_message": null
}
```

#### Get Servo History
```http
GET /controllers/servo/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "position": "OPEN",
      "timestamp": "2024-11-20T11:58:42.000Z"
    },
    {
      "position": "CLOSED",
      "timestamp": "2024-11-20T11:58:42.000Z"
    },
    {
      "position": "HALF_OPEN",
      "timestamp": "2024-11-20T11:58:42.000Z"
    },
    {
      "angle": 90,
      "timestamp": "2024-11-20T11:58:42.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

### LCD Controller

#### Get Latest LCD State
```http
GET /controllers/lcd/preview
```

**Response (200 OK):**
```json
{
  "message": "Hello World!",
  "duration": 10000,
  "timestamp": "2024-11-20T11:59:08.000Z"
}
```

#### Set LCD State
```http
POST /controllers/lcd
```

**Request Body:**
```json
{
  "message": "Hello World!",
  "duration": 10000
}
```

**Response (200 OK):**
```json
{
  "error": false,
  "error_message": null
}
```

#### Get LCD History
```http
GET /controllers/lcd/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "message": "Hello World!",
      "duration": 10000,
      "timestamp": "2024-11-20T11:59:08.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

### Fan Controller

#### Get Latest Fan State
```http
GET /controllers/fan/preview
```

**Response (200 OK):**
```json
{
  "speed": 140,
  "timestamp": "2024-11-20T11:53:44.000Z"
}
```

#### Set Fan State
```http
POST /controllers/fan
```

**Request Body:**
```json
{
  "speed": 140 // 0-255, 0 is off
}
```

**Response (200 OK):**
```json
{
  "error": false,
  "error_message": null
}
```

#### Get Fan History
```http
GET /controllers/fan/history
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)
- `start_time`: ISO datetime string
- `end_time`: ISO datetime string

**Response (200 OK):**
```json
{
  "data": [
    {
      "speed": 140,
      "timestamp": "2024-11-20T11:53:44.000Z"
    },
    {
      "speed": 0,
      "timestamp": "2024-11-20T11:53:44.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

## Rules Management

### Get All Rules
```http
GET /rules
```

**Query Parameters:**
- `page`: integer (default: 1)
- `per_page`: integer (default: 25)

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "trigger_sensor": "dht11.temperature.celsius",
      "op": ">",
      "threshold": 30.0,
      "target_controller": "fan",
      "action": "speed:140",
      "created_at": "2024-11-20T11:00:00.000Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "per_page": 25
  }
}
```

### Create Rule
```http
POST /rules
```

**Request Body:**
```json
{
  "trigger_sensor": "string",
  "op": "string",
  "threshold": float,
  "target_controller": "string",
  "action": "string"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "trigger_sensor": "string",
  "op": "string",
  "threshold": float,
  "target_controller": "string",
  "action": "string",
  "created_at": "2024-11-20T11:00:00.000Z"
}
```

### Get Rule by ID
```http
GET /rules/{rule_id}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "trigger_sensor": "string",
  "op": "string",
  "threshold": float,
  "target_controller": "string",
  "action": "string",
  "created_at": "2024-11-20T11:00:00.000Z"
}
```

### Update Rule
```http
PUT /rules/{rule_id}
```

**Request Body:** Same as Create Rule

**Response (200 OK):** Same as Get Rule

### Delete Rule
```http
DELETE /rules/{rule_id}
```

**Response (204 No Content)**

## Error Responses

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid input parameters",
  "details": {
    "field": ["error description"]
  }
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

### Controller-Specific Notes

1. **Buzzer Controller**
   - Tracks frequency (Hz) and duration (ms)
   - Active state indicates if buzzer is currently sounding
   - Typical frequency range: 20Hz - 20000Hz
   - Duration typically in milliseconds

2. **Relay Controller**
   - Simple binary state (active/inactive)
   - Used for controlling high-power devices
   - State changes are timestamped

3. **LED Controller**
   - Simple binary state (active/inactive)
   - Used for visual indicators
   - State changes are timestamped

4. **Servo Controller**
   - Position states can be "OPEN" or "CLOSED"
   - Used for mechanical movement control
   - Position changes are timestamped

5. **LCD Controller**
   - Tracks displayed message and duration
   - Duration in milliseconds
   - Message length may be limited based on LCD size
   - Updates are timestamped

Each controller endpoint follows these common patterns:
- All have both preview (latest state) and history endpoints
- All historical data is paginated
- All responses include timestamps
- All support time-range filtering
- All require authentication
- All follow the same error response format