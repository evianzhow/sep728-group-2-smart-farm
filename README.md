# IoT-Enabled Smart Farm Management System

## Architecture Explanation

This codebase contains three parts:

1. **ESP32 Onboard Software** under `esp32/` folder
   - This software is responsible for collecting data from the sensors and sending it to the cloud.
   - It also listens for commands from the cloud and controls the actuators accordingly.
2. **Intelligent Control System** backend under `smart_farm_backend/` folder
   - This software is responsible for processing the data from the sensors and sending control commands to the actuators.
3. **Frontend** under `smart_farm_frontend/` folder
   - This is a simple web app that allows the user to view the data from the sensors and control the actuators.
   - Support automation rule creation and deletion.

## How to run

1. Compile the ESP32 project with instructions from [here](https://docs.keyestudio.com/projects/KS0567/en/latest/wiki/index.html).
   - Be sure to install the specific version `2.0.6` of the board manager `esp32` by expressif system.
   - Download all the libraries from official wiki and add them to Arduino IDE.
   - In Arduino IDE, install external libraries: `PubSubClient`, `ezButton`, `ArduinoJson`.
   - In order to compile the project, create a file named `WifiCredentials.h` under `esp32/sketch_nov13a/` folder and add the following content:
     ```cpp
    // WiFi Configuration
    const char* ssid = "your_wifi_ssid";
    const char* pwd = "your_wifi_password";
     ```
2. Run the backend software under `smart_farm_backend/` folder.
   - Create a `.env` file and add the following content:
     ```
     MQTT_USERNAME=<your_mqtt_username>
     MQTT_PASSWORD=<your_mqtt_password>
     ```
   - Modify the `MQTT_BROKER` and `MQTT_PORT` in `app/config.py` with the current MQTT broker you are using.
   - Then, run it up with `docker compose up --build` to start the services. Service will be available at `http://<host>:8000`.
3. Run the frontend software under `smart_farm_frontend/` folder.
   - Be sure to change the backend service URL (`apiEndpoint`) in `smart_farm_frontend/src/App.vue` to the correct host and port.
   - The best way to run it is to use `npm install` to install the dependencies and then `npm run serve` to start the development server.
   - **OR**
   - Run `npm run build` to build the project and then install `npm install -g serve` and `serve -t dist/` to start the static server.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
