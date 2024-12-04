<template>
    <div>
      <h1>Smart FarmDashboard</h1>
      <p>Sensors:</p>
      <div class="card-container">
        <SensorCard 
          title="HUMIDITY" 
          :value="humidityValue + ' %'" 
          icon="💧" 
          color="blue" 
          @dblclick="navigateToDetails('HUMIDITY')"/>
        <SensorCard 
          title="ILLUMINATION" 
          :value="illuminationValue + ' %'" 
          icon="🌞" 
          color="red" 
          @dblclick="navigateToDetails('ILLUMINATION')"/>
        <SensorCard 
          title="TEMPERATURE" 
          :value="temperatureValue1 + ' C° / ' + temperatureValue2 + ' F° / ' + temperatureValue3 + ' k°'" 
          icon="🌡️" 
          color="orange" 
          @dblclick="navigateToDetails('TEMPERATURE')"/>
        <SensorCard 
          title="STEAM" 
          :value="steamValue + ' %'" 
          icon="🌤️" 
          color="blue" 
          @dblclick="navigateToDetails('STEAM')"/>
        <SensorCard 
          title="DEWPOINT" 
          :value="dewPointValue + ' C°'" 
          icon="💦" 
          color="red" 
          @dblclick="navigateToDetails('DEWPOINT')"/>
        <SensorCard 
          title="SOILHUMIDITY" 
          :value="soilHumidityValue + ' %'" 
          icon="🌱" 
          color="orange" 
          @dblclick="navigateToDetails('SOILHUMIDITY')"/>
        <SensorCard 
          title="WATERLEVEL" 
          :value="WaternValue + ' mm'" 
          icon="🌊" 
          color="blue" 
          @dblclick="navigateToDetails('WATERLEVEL')"/>
        <SensorCard 
          title="ULTRASONIC" 
          :value="ultrasonicValue + ' cm'" 
          icon="🔊" 
          color="red" 
          @dblclick="navigateToDetails('ULTRASONIC')"/>
        <!-- <SensorCard 
          title="PHOTORESISTOE" 
          value="Hardware Inavailable" 
          icon="📷" 
          color="orange" 
          @dblclick="handleUnavailableComponent" 
          /> -->
      </div>

      <p>Controllers:</p>
      <div class="toggle-container">
            <ToggleSwitch label="Passive Buzzer" 
            @dblclick="navigateToDetailsBuzzer()"/>
            <ToggleSwitch label="LCD" 
            @dblclick="navigateToDetailsLCD()"/>
            <CataSlider label="Servo" 
            @dblclick="navigateToDetailsServo()"/>
      </div>
      <div class="toggle-container">
            <NormalSwitch label="LED" 
            @dblclick="navigateToDetailsLED()"/>
            <NormalSwitch label="Relay Module" 
            @dblclick="navigateToDetailsRelay()"/>
            <RangeSlider label="Fan" 
            @dblclick="navigateToDetailsFan()"/>
      </div>
      <p>Status:</p>
      <div class="controls-container">    
            <ButtonStatus label="Button" 
            @dblclick="navigateToDetailsButton()"/>
            <ButtonStatus label="PIR" 
            @dblclick="navigateToDetailsPIR()"/>
      </div>

    </div>
  </template>
  
  <script>
  import SensorCard from './SensorCard.vue';
  import ToggleSwitch from './ToggleSwitch.vue';
  import RangeSlider from './RangeSlider.vue';
  import ButtonStatus from './ButtonStatus.vue';
  import NormalSwitch from './NormalSwitch.vue';
  import CataSlider from './CataSlider.vue';
  import axios from "axios";
  
  export default {
    name: "HomePage",
    components: {
      SensorCard,
      ToggleSwitch,
      RangeSlider,
      ButtonStatus,
      NormalSwitch,
      CataSlider,
    },
    inject: ["getAuthToken"],
    data() {
      return {
        intervalId: null, // Add this to store the interval ID
        authToken: "",
        illuminationValue: "Loading...", 
        WaternValue: "Loading...",
        steamValue: "Loading...",
        ultrasonicValue: "Loading...",
        temperatureValue1: "Loading...",
        temperatureValue2: "Loading...",
        temperatureValue3: "Loading...",
        humidityValue: "Loading...",
        dewPointValue: "Loading...",
        soilHumidityValue: "Loading...",
      };
  },
    methods: {
      navigateToDetails(title) {
      this.$router.push(`/sensor/${title}`); // Navigate to the sensor details page
    },
      handleUnavailableComponent() {
      alert("No this component"); // Show an alert when double-clicked
    },
      navigateToDetailsPIR(){
        this.$router.push({ name: 'PIRDetails' });
      },
      navigateToDetailsButton(){
        this.$router.push({ name: 'ButtonDetails' });
      },
      //------------------------------------------------
      navigateToDetailsBuzzer(){
        this.$router.push({ name: 'BuzzerDetails' });
      },
      navigateToDetailsLCD(){
        this.$router.push({ name: 'LCDDetails' });
      },
      navigateToDetailsServo(){
        this.$router.push({ name: 'ServoDetails' });
      },
      navigateToDetailsLED(){
        this.$router.push({ name: 'LEDDetails' });
      },
      navigateToDetailsRelay(){
        this.$router.push({ name: 'RelayDetails' });
      },
      navigateToDetailsFan(){
        this.$router.push({ name: 'FanDetails' });
      },
    //---------------Here to use API------------------------------
    //Soil humidity
    async fetchSoilHumidityValue() {
      try {
        const token = await this.getAuthToken(); 
        console.log("Token being used:", token); 
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/soil/preview",
          {
            headers: {
              Authorization: token, 
            },
          }
        );
        console.log("Response data:", response.data);
        this.soilHumidityValue = response.data.percentage; 
      } catch (error) {
        console.error("Error fetching soil humidity data:", error); 
        this.soilHumidityValue = "Error";
      }
    },
    //Dew Point
    async fetchDewPointValue() {
      try {
        const token = await this.getAuthToken(); 
        console.log("Token being used:", token); 
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/dht11/dewpoint/preview",
          {
            headers: {
              Authorization: token, 
            },
          }
        );
        console.log("Response data:", response.data);
        this.dewPointValue = parseFloat(response.data.dewpoint.celsius).toFixed(2); 
      } catch (error) {
        console.error("Error fetching dew point data:", error); 
        this.dewPointValue = "Error";
      }
    },
    //Humamidity
    async fetchHumidityValue() {
      try {
        const token = await this.getAuthToken(); 
        console.log("Token being used:", token); 
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/dht11/humidity/preview",
          {
            headers: {
              Authorization: token, 
            },
          }
        );
        console.log("Response data:", response.data);
        this.humidityValue = response.data.humidity.value; 
      } catch (error) {
        console.error("Error fetching humidity data:", error); 
        this.humidityValue = "Error";
      }
    },
    //Illumination
        async fetchIlluminationValue() {
      try {
        const token = await this.getAuthToken(); 
        console.log("Token being used:", token); 
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/light/preview",
          {
            headers: {
              Authorization: token, 
            },
          }
        );
        console.log("Response data:", response.data);
        this.illuminationValue = response.data.percentage; 
      } catch (error) {
        if (error.response) {
          console.error("Error response from server:", error.response.data);
          this.illuminationValue = "Server Error"; 
        } else if (error.request) {
          console.error("No response received from server:", error.request);
          this.illuminationValue = "Connection Error"; 
        } else {
          console.error("Unexpected error:", error.message);
          this.illuminationValue = "Unexpected Error"; 
        }
        this.illuminationValue = "Error";
      }
    },
    //Water
    async fetchWaterValue() {
      try {
        const token = await this.getAuthToken(); 
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/water/preview",
          {
            headers: {
              Authorization: token, 
            },
          }
        );
        this.WaternValue = response.data.value; 
      } catch (error) {
        console.error("Error fetching water data:", error);
        this.WaternValue = "Error"; 
      }
    },
    //Steam
    async fetchSteamValue() {
      try {
        const token = await this.getAuthToken(); 
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/steam/preview",
          {
            headers: {
              Authorization: token, 
            },
          }
        );
        this.steamValue = response.data.value; 
      } catch (error) {
        console.error("Error fetching steam data:", error);
        this.steamValue = "Error"; 
      }
    },
    //ultrasonic
    async fetchUltrasonicValue() {
      try {
        const token = await this.getAuthToken(); 
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/ultrasonic/preview",
          {
            headers: {
              Authorization: token, 
            },
          }
        );
        this.ultrasonicValue = response.data.value; 
      } catch (error) {
        console.error("Error fetching ultrasonic data:", error);
        this.ultrasonicValue = "Error"; 
      }
    },
    //temperature
    async fetchTemperatureValue() {
      try {
        const token = await this.getAuthToken(); 
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/dht11/temperature/preview",
          {
            headers: {
              Authorization: token, 
            },
          }
        );
        this.temperatureValue1 = response.data.temperature.celsius; 
        this.temperatureValue2 = response.data.temperature.fahrenheit;
        this.temperatureValue3 = response.data.temperature.kelvin;
      } catch (error) {
        console.error("Error fetching ultrasonic data:", error);
        this.temperatureValue1 = "Error"; 
        this.temperatureValue2 = "Error"; 
        this.temperatureValue3 = "Error"; 
      }
    },
    //------------------------------------------------------------
    },
    async mounted() {
      this.intervalId = setInterval(async () => {
        await this.fetchIlluminationValue(); 
        await this.fetchWaterValue();
        await this.fetchSteamValue();
        await this.fetchUltrasonicValue();
        await this.fetchTemperatureValue();
        await this.fetchHumidityValue();
        await this.fetchDewPointValue();
        await this.fetchSoilHumidityValue();
      }, 5000);
    },
    unmounted() {
      // Clear the interval when component is unmounted
      if (this.intervalId) {
        clearInterval(this.intervalId);
      }
    },
  };

  </script>
  
  <style scoped>
  .card-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Three cards per row */
  gap: 10px; /* Smaller gap between cards */
}

  .toggle-container {
  margin-top: 30px;
  display: flex;
  align-items: flex-start; /* Align switches to the left */
  gap: 20px; /* Add spacing between switches */
}
    .controls-container {
    margin-top: 30px;
    display: flex;
    gap: 20px;
    align-items: flex-start; /* Align switches to the left */
    }
  </style>
  