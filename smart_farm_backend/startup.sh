#!/bin/bash
# startup.sh

# Make the script executable
set -e

# Run database initialization
python init_db.py

# Start the main application
python run.py --mqtt-username "${MQTT_USERNAME}" --mqtt-password "${MQTT_PASSWORD}"