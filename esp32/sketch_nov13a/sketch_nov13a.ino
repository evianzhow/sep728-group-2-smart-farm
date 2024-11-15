#include <Arduino.h>
#ifdef ESP32
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif

#include <WiFiClientSecure.h>
#include <PubSubClient.h>  // Add MQTT library
#include <ArduinoJson.h>   // Add JSON library for MQTT payloads
#include <dht11.h>
#include <analogWrite.h>
#include <ESP32_Servo.h>
#include <LiquidCrystal_I2C.h>
#include "WifiCredentials.h"
#include <time.h>

// Pin Definitions (unchanged)
#define DHT11PIN        17
#define RAINWATERPIN    35
#define LIGHTPIN        34
#define WATERLEVELPIN   33
#define SOILHUMIDITYPIN 32
#define LEDPIN          27
#define RELAYPIN        25
#define SERVOPIN        26
#define FANPIN1         19
#define FANPIN2         18
#define BUZZERPIN       16

#define TZ_America_New_York	PSTR("EST5EDT,M3.2.0,M11.1.0")

// and MQTT Configuration
const char* mqtt_server = "06a68c084516440da5d6c84b6514ed49.s1.eu.hivemq.cloud";  // Replace with your MQTT broker
const int mqtt_port = 8883;
const char* mqtt_user = "esp32";       // If required
const char* mqtt_password = "h4pPyhack!ng";   // If required
const char* device_id = "esp32_01";           // Unique device ID

// MQTT Topics
char topic_buffer[128];
#define MQTT_BASE_TOPIC "farm/%s"
#define MQTT_BUFFER_SIZE 256

// Initialize objects
LiquidCrystal_I2C lcd(0x27,16,2);
WiFiClientSecure espClient;
PubSubClient mqtt(espClient);
dht11 DHT11;
Servo myservo;

// Variables for sensor values
int Temperature, Humidity, SoilHumidity, Light, WaterLevel, Rainwater;
unsigned long lastPublish = 0;
const unsigned long publishInterval = 5000; // Publish every 5 seconds

unsigned long lcdMessageTimeout = 0;
String lcdCustomMessage = "";
bool lastMqttState = false;

// Function declarations
void setupMQTT();
void reconnectMQTT();
void publishSensorData();
void handleMQTTCallback(char* topic, byte* payload, unsigned int length);
String createTopic(const char* component, const char* action);

void setDateTime() {
  // You can use your own timezone, but the exact time is not used at all.
  // Only the date is needed for validating the certificates.
  configTzTime(TZ_America_New_York, "pool.ntp.org", "time.nist.gov");

  Serial.print("Waiting for NTP time sync: ");
  time_t now = time(nullptr);
  while (now < 8 * 3600 * 2) {
    delay(100);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println();

  struct tm timeinfo;
  gmtime_r(&now, &timeinfo);
  Serial.printf("%s %s", tzname[0], asctime(&timeinfo));
}

void setup() {
  Serial.begin(9600);
  
  // Connect to WiFi
  WiFi.begin(ssid, pwd);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");

  // FIXME: Use this only for testing, it allows connecting without a root certificate
  // FIXME: This may hinder our experimental with MQTT safety features
  // https://arduino.stackexchange.com/questions/72684/how-to-connect-to-mqtt-broker-with-tls
  // https://console.hivemq.cloud/clients/arduino-esp8266?uuid=06a68c084516440da5d6c84b6514ed49&clusterType=free&image=/assets/guides/arduino.svg
  espClient.setInsecure();
  
  // Initialize NTP Client
  setDateTime();

  // Initialize MQTT
  setupMQTT();
  
  // Initialize LCD
  lcd.init();
  lcd.backlight();
  updateLCDStatus();

  // Initialize pins
  pinMode(LEDPIN, OUTPUT);
  pinMode(RAINWATERPIN, INPUT);
  pinMode(LIGHTPIN, INPUT);
  pinMode(SOILHUMIDITYPIN, INPUT);
  pinMode(WATERLEVELPIN, INPUT);
  pinMode(RELAYPIN, OUTPUT);
  pinMode(FANPIN1, OUTPUT);
  pinMode(FANPIN2, OUTPUT);
  pinMode(BUZZERPIN, OUTPUT);
  
  myservo.attach(SERVOPIN);
}

// Add this new function
void updateLCDStatus() {
  lcd.clear();
  lcd.setCursor(0, 0);
  if (WiFi.status() == WL_CONNECTED) {
    lcd.print(WiFi.localIP());
  } else {
    lcd.print("Disconnected");
  }
  
  lcd.setCursor(0, 1);
  if (lcdCustomMessage != "" && millis() < lcdMessageTimeout) {
    lcd.print(lcdCustomMessage);
  } else {
    lcdCustomMessage = ""; // Clear the message
    if (mqtt.connected()) {
      lcd.print("MQTT:OK");
    } else {
      lcd.print("MQTT:NC");
    }
  }
}

void loop() {
  if (!mqtt.connected()) {
    reconnectMQTT();
  }
  mqtt.loop();

  // Add to loop() after mqtt.loop():
  if (lastMqttState != mqtt.connected() || WiFi.status() != WL_CONNECTED) {
    updateLCDStatus();
    lastMqttState = mqtt.connected();
  }

  if (lcdMessageTimeout > 0 && millis() > lcdMessageTimeout) {
    lcdMessageTimeout = 0;
    updateLCDStatus();
  }

  // Publish sensor data periodically
  if (millis() - lastPublish > publishInterval) {
    getSensorsData();
    publishSensorData();
    lastPublish = millis();
  }
}

void setupMQTT() {
  mqtt.setServer(mqtt_server, mqtt_port);
  mqtt.setCallback(handleMQTTCallback);
}

void reconnectMQTT() {
  while (!mqtt.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (mqtt.connect(device_id, mqtt_user, mqtt_password)) {
      Serial.println("Connected to MQTT broker");
      
      // Subscribe to control topics
      mqtt.subscribe(createTopic("led", "cmd").c_str());
      mqtt.subscribe(createTopic("relay", "cmd").c_str());
      mqtt.subscribe(createTopic("fan", "cmd").c_str());
      mqtt.subscribe(createTopic("servo", "cmd").c_str());
      mqtt.subscribe(createTopic("buzzer", "cmd").c_str());
      mqtt.subscribe(createTopic("lcd", "cmd").c_str());
    } else {
      Serial.print("Failed, rc=");
      Serial.print(mqtt.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

String createTopic(const char* component, const char* action) {
  sprintf(topic_buffer, "farm/%s/%s/%s", device_id, component, action);
  return String(topic_buffer);
}

void publishSensorData() {
  StaticJsonDocument<512> doc;
  char mqtt_payload[MQTT_BUFFER_SIZE];
  
  // Publish DHT11 data
  doc.clear();
  JsonObject humidity = doc.createNestedObject("humidity");
  humidity["value"] = Humidity;
  humidity["unit"] = "%";
  JsonObject temperature = doc.createNestedObject("temperature");
  temperature["celsius"] = Temperature;
  temperature["fahrenheit"] = (Temperature * 9.0/5.0) + 32;
  temperature["kelvin"] = Temperature + 273.15;
  serializeJson(doc, mqtt_payload);
  mqtt.publish(createTopic("dht11", "state").c_str(), mqtt_payload);

  // Publish soil humidity
  doc.clear();
  doc["raw"] = SoilHumidity;
  doc["percentage"] = map(SoilHumidity, 0, 4095, 0, 100);
  serializeJson(doc, mqtt_payload);
  mqtt.publish(createTopic("soil", "state").c_str(), mqtt_payload);

  // Publish light level
  doc.clear();
  doc["value"] = Light;
  doc["percentage"] = map(Light, 0, 4095, 0, 100);
  serializeJson(doc, mqtt_payload);
  mqtt.publish(createTopic("light", "state").c_str(), mqtt_payload);

  // Publish water level
  doc.clear();
  doc["raw"] = WaterLevel;
  doc["percentage"] = map(WaterLevel, 0, 4095, 0, 100);
  serializeJson(doc, mqtt_payload);
  mqtt.publish(createTopic("water", "state").c_str(), mqtt_payload);

  // Publish steam sensor data
  doc.clear();
  doc["value"] = Rainwater;
  doc["percentage"] = map(Rainwater, 0, 4095, 0, 100);
  serializeJson(doc, mqtt_payload);
  mqtt.publish(createTopic("steam", "state").c_str(), mqtt_payload);
}

void handleMQTTCallback(char* topic, byte* payload, unsigned int length) {
  StaticJsonDocument<200> doc;
  char json[length + 1];
  memcpy(json, payload, length);
  json[length] = '\0';
  
  DeserializationError error = deserializeJson(doc, json);
  if (error) {
    Serial.println("Failed to parse JSON");
    return;
  }

  String topicStr = String(topic);

  // LED control
  if (topicStr == createTopic("led", "cmd")) {
    bool active = doc["active"];
    digitalWrite(LEDPIN, active ? HIGH : LOW);
    mqtt.publish(createTopic("led", "state").c_str(), json);
  }
  
  // Relay (water pump) control
  else if (topicStr == createTopic("relay", "cmd")) {
    bool active = doc["active"];
    digitalWrite(RELAYPIN, active ? HIGH : LOW);
    if (active) {
      delay(400);
      digitalWrite(RELAYPIN, LOW);
      delay(650);
    }
    mqtt.publish(createTopic("relay", "state").c_str(), json);
  }
  
  // Fan control
  else if (topicStr == createTopic("fan", "cmd")) {
    int speed = doc["speed"];
    if (speed > 0) {
      analogWrite(FANPIN1, speed);
      digitalWrite(FANPIN2, LOW);
    } else {
      digitalWrite(FANPIN1, LOW);
      digitalWrite(FANPIN2, LOW);
    }
    mqtt.publish(createTopic("fan", "state").c_str(), json);
  }
  
  // Servo control
  else if (topicStr == createTopic("servo", "cmd")) {
    if (doc.containsKey("angle")) {
      int angle = doc["angle"];
      myservo.write(angle);
    } else if (doc.containsKey("position")) {
      const char* position = doc["position"];
      if (strcmp(position, "OPEN") == 0) myservo.write(80);
      else if (strcmp(position, "HALF_OPEN") == 0) myservo.write(120);
      else if (strcmp(position, "CLOSED") == 0) myservo.write(180);
    }
    mqtt.publish(createTopic("servo", "state").c_str(), json);
  }
  
  // Buzzer control
  else if (topicStr == createTopic("buzzer", "cmd")) {
    int frequency = doc["frequency"] | 0;  // Default to 0 if not specified
    int duration = doc["duration"] | 0;    // Default to 0 if not specified
    
    // Create state payload
    StaticJsonDocument<200> stateDoc;
    stateDoc["active"] = (frequency > 0 && duration > 0);
    stateDoc["frequency"] = frequency;
    stateDoc["duration"] = duration;
    
    char statePayload[200];
    serializeJson(stateDoc, statePayload);
    mqtt.publish(createTopic("buzzer", "state").c_str(), statePayload);
    
    // Control buzzer
    controlBuzzer(frequency, duration);
  }

  // LCD control
  else if (topicStr == createTopic("lcd", "cmd")) {
    const char* message = doc["message"] | "";
    int duration = doc["duration"] | 10; // Default 10 seconds if not specified
    
    // Create state payload
    StaticJsonDocument<200> stateDoc;
    stateDoc["message"] = message;
    stateDoc["duration"] = duration;
    
    char statePayload[200];
    serializeJson(stateDoc, statePayload);
    mqtt.publish(createTopic("lcd", "state").c_str(), statePayload);
    
    // Update LCD
    updateLCDWithMessage(message, duration);
  }
}

void getSensorsData() {
  // Original sensor reading code
  int chk = DHT11.read(DHT11PIN);
  Rainwater = analogRead(RAINWATERPIN);
  Light = analogRead(LIGHTPIN);
  SoilHumidity = analogRead(SOILHUMIDITYPIN) * 2.3;
  WaterLevel = analogRead(WATERLEVELPIN) * 2.5;
  Temperature = DHT11.temperature;
  Humidity = DHT11.humidity;
}

// Add new buzzer control function
void controlBuzzer(int frequency, int duration) {
  if (frequency > 0 && duration > 0) {
    // Calculate period in microseconds
    int period = 1000000 / frequency;  // Convert frequency to period in microseconds
    int halfPeriod = period / 2;
    long endTime = millis() + duration;
    
    // Generate square wave for the specified duration
    while (millis() < endTime) {
      digitalWrite(BUZZERPIN, HIGH);
      delayMicroseconds(halfPeriod);
      digitalWrite(BUZZERPIN, LOW);
      delayMicroseconds(halfPeriod);
    }
  }
  digitalWrite(BUZZERPIN, LOW);  // Ensure buzzer is off after completion
}

// Add new function to update LCD with temporary message
void updateLCDWithMessage(const String& message, int duration) {
  lcdCustomMessage = message;
  lcdMessageTimeout = millis() + (duration * 1000); // Convert to milliseconds
  lcd.setCursor(0, 1);
  lcd.print("                "); // Clear line first
  lcd.setCursor(0, 1);
  lcd.print(message);
}