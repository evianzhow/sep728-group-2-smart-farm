<template>
  <div class="sensor-details">
    <h1>{{ title }}</h1>
    <div class="chart-container">
      <p>Historical Data (Latest 24 hours Average)</p>

      <!-- Conditional rendering for Illumination -->
      <apexchart
        v-if="title === 'ILLUMINATION'"
        ref="illuminationChart"
        type="line"
        :options="illuminationChartOptions"
        :series="illuminationChartSeries"
      />
      
      <!-- Conditional rendering for Dew Point -->
      <apexchart
        v-if="title === 'DEWPOINT'"
        ref="dewPointChart"
        type="line"
        :options="dewPointChartOptions"
        :series="dewPointChartSeries"
      />

      <!-- Step1: Add more "apexchart" components for other sensors -->
      <!-- Follow the same structure used above for Illumination and Dew Point -->
      <!-- Example for another sensor: Temperature -->
      
      <apexchart
        v-if="title === 'TEMPERATURE'"
        ref="temperatureChart"
        type="line"
        :options="temperatureChartOptions"
        :series="temperatureChartSeries"
      />
      <apexchart
        v-if="title === 'HUMIDITY'"
        ref="humidityChart"
        type="line"
        :options="humidityChartOptions"
        :series="humidityChartSeries"
      />
      <apexchart
        v-if="title === 'STEAM'"
        ref="steamChart"
        type="line"
        :options="steamChartOptions"
        :series="steamChartSeries"
      />
      <apexchart
        v-if="title === 'SOILHUMIDITY'"
        ref="soilChart"
        type="line"
        :options="soilChartOptions"
        :series="soilChartSeries"
      />
      <apexchart
        v-if="title === 'WATERLEVEL'"
        ref="waterChart"
        type="line"
        :options="waterChartOptions"
        :series="waterChartSeries"
      />
      <apexchart
        v-if="title === 'ULTRASONIC'"
        ref="ultrasonicChart"
        type="line"
        :options="ultrasonicChartOptions"
        :series="ultrasonicChartSeries"
      />
      
    </div>

    <!-- Button to return to the home page -->
    <button @click="goHome">Return to Home</button>
  </div>
</template>

<script>
// Import necessary libraries
import VueApexCharts from "vue3-apexcharts"; // For chart rendering
import axios from "axios"; // For HTTP requests

export default {
  name: "SensorDetails", // Component name
  inject: ["getAuthToken", "apiEndpoint"], // Inject auth token for secure API calls
  components: {
    apexchart: VueApexCharts, // Register the ApexCharts component
  },
  data() {
    return {
      // Static data for each sensor
      sensorData: {
        HUMIDITY: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], //Done ^^^
        ILLUMINATION: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], //Done
        TEMPERATURE: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], //Done
        STEAM: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],//Done
        DEWPOINT: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // Done
        SOILHUMIDITY: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        WATERLEVEL: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],//Done
        ULTRASONIC: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],//Done ^^^
        PHOTORESISTOE: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // No need to handle this one
      },

      ultrasonicChartSeries: [],
      ultrasonicChartOptions: {
        chart: {
          height: 300,
          type: "line",
        },
        xaxis: {
          categories: [], 
        },
        title: {
          text: "Ultrasonic Distance Historical Data",
          align: "center",
        },
        colors: ["#2d6d92"], 
      },

      waterChartSeries: [],
      waterChartOptions: {
        chart: {
          height: 300,
          type: "line",
        },
        xaxis: {
          categories: [], 
        },
        title: {
          text: "Water Level Historical Data",
          align: "center",
        },
        colors: ["#2d6d92"], 
      },

      soilChartSeries: [],
      soilChartOptions: {
        chart: {
          height: 300,
          type: "line",
        },
        xaxis: {
          categories: [], 
        },
        title: {
          text: "Soil Humidity Historical Data",
          align: "center",
        },
        colors: ["#2d6d92"], 
      },

      steamChartSeries: [],
      steamChartOptions: {
        chart: {
          height: 300,
          type: "line",
        },
        xaxis: {
          categories: [], 
        },
        title: {
          text: "Steam Historical Data",
          align: "center",
        },
        colors: ["#2d6d92"], 
      },

      // Chart configuration for Illumination
      illuminationChartSeries: [],
      illuminationChartOptions: {
        chart: {
          height: 300,
          type: "line",
        },
        xaxis: {
          categories: [], // Categories for the x-axis (timestamps)
        },
        title: {
          text: "Illumination Historical Data",
          align: "center",
        },
        colors: ["#2d6d92"], // Chart line color for Illumination
      },

      // Chart configuration for Dew Point
      dewPointChartSeries: [],
      dewPointChartOptions: {
        chart: {
          height: 300,
          type: "line",
        },
        xaxis: {
          categories: [], // Categories for the x-axis (timestamps)
        },
        title: {
          text: "Dew Point Historical Data",
          align: "center",
        },
        colors: ["#0000FF"], // Chart line color for Dew Point
      },

      // Step2: Define chart options and series for other sensors like Temperature, etc.
      // Example for Temperature (uncomment to implement):
      
      temperatureChartSeries: [],
      temperatureChartOptions: {
        chart: {
          height: 300,
          type: "line",
        },
        xaxis: {
          categories: [],
        },
        title: {
          text: "Temperature Historical Data",
          align: "center",
        },
        colors: ["#FF5733"],
      },
      humidityChartSeries: [],
      humidityChartOptions: {
        chart: {
          height: 300,
          type: "line",
        },
        xaxis: {
          categories: [],
        },
        title: {
          text: "Humidity Historical Data",
          align: "center",
        },
        colors: ["#FF5733"],
      },
      
    };
  },

  computed: {
    title() {
      // Dynamically retrieve the title from the route parameters
      return this.$route.params.title || "Sensor Details"; 
    },
  },

  methods: {
    // Method to navigate back to the home page
    goHome() {
      this.$router.push("/home"); 
    },

    // Refresh a chart with new data and options
    forceRefreshChart(chartRef, chartSeries, chartOptions) {
      if (chartRef) {
        chartRef.updateSeries(chartSeries, true); // Update the series data
        chartRef.updateOptions(chartOptions, true); // Update the chart options
      }
    },

    // Step 3: Fetch historical data for sensors
    // Example fetch method for Light (percentage type)
    async fetchHumidityHistory() {
      try {
        const token = await this.getAuthToken(); // Get the auth token
        const response = await axios.get(
          `${this.apiEndpoint}/sensors/dht11/humidity/chart`, // API URL
          {
            headers: { Authorization: token }, // Pass token in the header
            params: {
              start_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 24 hours ago
              end_time: new Date().toISOString(), // Current time
              interval: "hour",
            },
          }
        );
        const historyData = response.data.data.map((entry) => ({
          timestamp: entry.timestamp,
          value: entry.value.toFixed(2), 
        }));

        // Assign data to the appropriate sensor array
        this.HUMIDITY = historyData;
        console.log("HUMIDITY Data:", this.HUMIDITY);
        this.updateHumidityChartData(); // Update chart with new data
      } catch (error) {
        console.error("Error fetching humidity history:", error);
      }
    },

    async fetchSoilHistory() {
      try {
        const token = await this.getAuthToken(); // Get the auth token
        const response = await axios.get(
          `${this.apiEndpoint}/sensors/soil/chart`, // API URL
          {
            headers: { Authorization: token }, // Pass token in the header
            params: {
              start_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 24 hours ago
              end_time: new Date().toISOString(), // Current time
              interval: "hour",
            },
          }
        );
        const historyData = response.data.data.map((entry) => ({
          timestamp: entry.timestamp,
          value: entry.value.toFixed(2), 
        }));

        // Assign data to the appropriate sensor array
        this.SOILHUMIDITY = historyData;
        console.log("SOIL HUMIDITY Data:", this.SOILHUMIDITY);
        this.updateSoilChartData(); // Update chart with new data
      } catch (error) {
        console.error("Error fetching soil humidity history:", error);
      }
    },

    async fetchSteamHistory() {
      try {
        const token = await this.getAuthToken(); // Get the auth token
        const response = await axios.get(
          `${this.apiEndpoint}/sensors/steam/chart`, // API URL
          {
            headers: { Authorization: token }, // Pass token in the header
            params: {
              start_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 24 hours ago
              end_time: new Date().toISOString(), // Current time
              interval: "hour",
            },
          }
        );
        const historyData = response.data.data.map((entry) => ({
          timestamp: entry.timestamp,
          percentage: entry.percentage.toFixed(2), // Process percentage data
        }));

        // Assign data to the appropriate sensor array
        this.STEAM = historyData;
        console.log("STEAM Data:", this.ILLUMINATION);
        this.updateSteamChartData(); // Update chart with new data
      } catch (error) {
        console.error("Error fetching steam history:", error);
      }
    },

    async fetchLightHistory() {
  try {
    const token = await this.getAuthToken(); // Get the auth token
    const response = await axios.get(
      `${this.apiEndpoint}/sensors/light/chart`, // API URL
      {
        headers: { Authorization: token }, // Pass token in the header
        params: {
          start_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 24 hours ago
          end_time: new Date().toISOString(), // Current time
          interval: "hour", // Use "hour" as the default interval
        },
      }
    );

    // Process the response data
    const historyData = response.data.data.map((entry) => ({
      timestamp: new Date(entry.timestamp).toLocaleString(), // Convert Unix timestamp to readable format
      percentage: entry.percentage.toFixed(2), // Round percentage to two decimal places
      value: entry.value, // Include raw value for completeness
    }));

    console.log("Light Chart Data:", historyData);

    // Store the processed data
    this.ILLUMINATION = historyData; // Assuming LIGHT_HISTORY is a reactive property for storing data
    this.updateIlluminatiionChartData(); // Call a method to update the chart
  } catch (error) {
    console.error("Error fetching light chart data:", error);
  }
},


    // Example fetch method for Dew Point
    async fetchDewPointHistory() {
      try {
        const token = await this.getAuthToken(); // Get auth token
        const response = await axios.get(
          `${this.apiEndpoint}/sensors/dht11/dewpoint/chart`, // API URL for Dew Point
          {
            headers: { Authorization: token },
            params: {
              start_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
              end_time: new Date().toISOString(),
              interval: "hour",
              unit: "celsius"
            },
          }
        );

        console.log("Raw Response Data:", response.data.data);

        // Process the data for Dew Point
        const historyData = response.data.data.map((entry) => ({
          timestamp: entry.timestamp,
          value: parseFloat(entry.value).toFixed(2),
        }));

        // Filter out null values
        this.DEWPOINT = historyData.filter((entry) => entry.value);
        this.updateDewPointChartData(); // Update Dew Point chart with new data
      } catch (error) {
        console.error("Error fetching dew point history:", error);
      }
    },

    async fetchWaterHistory() {
      try {
        const token = await this.getAuthToken(); // Get the auth token
        const response = await axios.get(
          `${this.apiEndpoint}/sensors/water/chart`, // API URL
          {
            headers: { Authorization: token }, // Pass token in the header
            params: {
              start_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 24 hours ago
              end_time: new Date().toISOString(), // Current time
              interval: "hour",
            },
          }
        );
        const historyData = response.data.data.map((entry) => ({
          timestamp: entry.timestamp,
          value: (entry.value).toFixed(2), 
        }));

        // Assign data to the appropriate sensor array
        this.WATERLEVEL = historyData;
        console.log("Water Data:", this.WATERLEVEL);
        this.updateWaterChartData(); // Update chart with new data
      } catch (error) {
        console.error("Error fetching water history:", error);
      }
    },

    async fetchUltrasonicHistory() {
      try {
        const token = await this.getAuthToken(); // Get the auth token
        const response = await axios.get(
          `${this.apiEndpoint}/sensors/ultrasonic/chart`, // API URL
          {
            headers: { Authorization: token }, // Pass token in the header
            params: {
              start_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 24 hours ago
              end_time: new Date().toISOString(), // Current time
              interval: "hour",
            },
          }
        );
        const historyData = response.data.data.map((entry) => ({
          timestamp: entry.timestamp,
          value: parseFloat(entry.value).toFixed(2), 
        }));

        // Assign data to the appropriate sensor array
        this.ULTRASONIC = historyData;
        console.log("Ultrasonic Data:", this.ULTRASONIC);
        this.updateUltrasonicChartData(); // Update chart with new data
      } catch (error) {
        console.error("Error fetching ultrasonic history:", error);
      }
    },

    async fetchTemperatureHistory() {
      try {
        const token = await this.getAuthToken(); 
        const response = await axios.get(
          `${this.apiEndpoint}/sensors/dht11/temperature/chart`, // API URL for Dew Point
          {
            headers: { Authorization: token },
            params: {
              start_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
              end_time: new Date().toISOString(),
              interval: "hour",
              unit: "celsius"
            },
          }
        );

        console.log("Raw Response Data:", response.data.data);

        const historyData = response.data.data.map((entry) => ({
          timestamp: entry.timestamp,
          value: parseFloat(entry.value).toFixed(2),
        }));

        this.TEMPERATURE = historyData.filter((entry) => entry.value !== null);
        this.updateTemperatureChartData();
      } catch (error) {
        console.error("Error fetching temperature history:", error);
      }
    },

    // Step 4: Update the chart data for Illumination
    updateWaterChartData() {
      const dataArray = this.WATERLEVEL.map((item) => parseFloat(item.value));
      const timeArray = this.WATERLEVEL.map((item) =>
        new Date(item.timestamp).toLocaleTimeString() || "Invalid Date"
      );

      console.log("Chart Data Array:", dataArray);
      console.log("Chart Time Array:", timeArray);

      this.waterChartSeries = [{ name: "Water Percentage", data: dataArray }];
      this.waterChartOptions.xaxis.categories = timeArray;
      this.forceRefreshChart(this.$refs.waterChart, this.waterChartSeries, this.waterChartOptions);
    },
    updateHumidityChartData() {
      const dataArray = this.HUMIDITY.map((item) => parseFloat(item.value));
      const timeArray = this.HUMIDITY.map((item) =>
        new Date(item.timestamp).toLocaleTimeString() || "Invalid Date"
      );

      console.log("Chart Data Array:", dataArray);
      console.log("Chart Time Array:", timeArray);

      this.humidityChartSeries = [{ name: "Humidity Percentage", data: dataArray }];
      this.humidityChartOptions.xaxis.categories = timeArray;
      this.forceRefreshChart(this.$refs.humidityChart, this.humidityChartSeries, this.humidityChartOptions);
    },
    updateSoilChartData() {
      const dataArray = this.SOILHUMIDITY.map((item) => parseFloat(item.percentage || 0));
      const timeArray = this.SOILHUMIDITY.map((item) =>
        new Date(item.timestamp).toLocaleTimeString() || "Invalid Date"
      );

      console.log("Chart Data Array:", dataArray);
      console.log("Chart Time Array:", timeArray);

      this.soilChartSeries = [{ name: "Soil Humidity Percentage", data: dataArray }];
      this.soilChartOptions.xaxis.categories = timeArray;
      //this.$refs.soilChart.updateSeries(this.soilChartSeries, true);
      //this.$refs.soilChart.updateOptions(this.soilChartOptions, true);
      this.forceRefreshChart(this.$refs.soilChart, this.soilChartSeries, this.soilChartOptions);
    },
    updateSteamChartData() {
      const dataArray = this.STEAM.map((item) => parseFloat(item.percentage || 0));
      const timeArray = this.STEAM.map((item) =>
        new Date(item.timestamp).toLocaleTimeString() || "Invalid Date"
      );

      console.log("Chart Data Array:", dataArray);
      console.log("Chart Time Array:", timeArray);

      this.steamChartSeries = [{ name: "Steam Percentage", data: dataArray }];
      this.steamChartOptions.xaxis.categories = timeArray;
      this.forceRefreshChart(this.$refs.steamChart, this.steamChartSeries, this.steamChartOptions);
    },
    //Illuminatiion
    updateIlluminatiionChartData() {
      const dataArray = this.ILLUMINATION.map((item) => parseFloat(item.percentage || 0));
      const timeArray = this.ILLUMINATION.map((item) =>
        new Date(item.timestamp).toLocaleTimeString() || "Invalid Date"
      );

      console.log("Chart Data Array:", dataArray);
      console.log("Chart Time Array:", timeArray);

      this.illuminationChartSeries = [{ name: "Light Percentage", data: dataArray }];
      this.illuminationChartOptions.xaxis.categories = timeArray;

      this.forceRefreshChart(this.$refs.illuminationChart, this.illuminationChartSeries, this.illuminationChartOptions);
    },
    //Temperature
    updateTemperatureChartData() {
      const dataArray = this.TEMPERATURE.map((item) => parseFloat(item.value));
      const timeArray = this.TEMPERATURE.map((item) =>
        new Date(item.timestamp).toLocaleTimeString() || "Invalid Date"
      );

      console.log("Temperature Data Array:", dataArray);
      console.log("Temperature Time Array:", timeArray);

      this.temperatureChartSeries = [{ name: "Temperature (°C)", data: dataArray }];
      this.temperatureChartOptions.xaxis.categories = timeArray;
      this.$refs.temperatureChart.updateSeries(this.temperatureChartSeries, true);
      this.$refs.temperatureChart.updateOptions(this.temperatureChartOptions, true);
      this.forceRefreshChart(this.$refs.temperaturetChart, this.temperatureChartSeries, this.temperatureChartOptions);
    },
    //Dew Point
    updateDewPointChartData() {
      const dataArray = this.DEWPOINT.map((item) => parseFloat(item.value));
      const timeArray = this.DEWPOINT.map((item) =>
        new Date(item.timestamp).toLocaleTimeString() || "Invalid Date"
      );

      console.log("Dew Point Data Array:", dataArray);
      console.log("Dew Point Time Array:", timeArray);

      // Update the Dew Point chart series with the processed data
      this.dewPointChartSeries = [{ name: "Dew Point (°C)", data: dataArray }];
      this.dewPointChartOptions.xaxis.categories = timeArray;
      this.forceRefreshChart(this.$refs.dewPointChart, this.dewPointChartSeries, this.dewPointChartOptions);
    },
    updateUltrasonicChartData() {
      const dataArray = this.ULTRASONIC.map((item) => parseFloat(item.value));
      const timeArray = this.ULTRASONIC.map((item) =>
        new Date(item.timestamp).toLocaleTimeString() || "Invalid Date"
      );

      console.log("Ultrasonic Data Array:", dataArray);
      console.log("Ultrasonic Time Array:", timeArray);

      this.ultrasonicChartSeries = [{ name: "Ultrasonic", data: dataArray }];
      this.ultrasonicChartOptions.xaxis.categories = timeArray;
      this.$refs.ultrasonicChart.updateOptions(this.ultrasonicChartOptions, true);
      this.forceRefreshChart(this.$refs.ultrasonicChart, this.ultrasonicChartSeries, this.ultrasonicOptions);
    },
  },

  mounted() {
    // Fetch historical data for Illumination and Dew Point
    if (this.title === "ILLUMINATION") {  
      this.fetchLightHistory();
    } else if (this.title === "DEWPOINT") {
      this.fetchDewPointHistory();
    } else if (this.title === "TEMPERATURE") {
      this.fetchTemperatureHistory();
    } else if (this.title === "HUMIDITY") {
      this.fetchHumidityHistory();
    } else if (this.title === "WATERLEVEL") {
      this.fetchWaterHistory();
    } else if (this.title === "STEAM") {
      this.fetchSteamHistory();
    } else if (this.title === "ULTRASONIC") {
      this.fetchUltrasonicHistory();
    } else if (this.title === "SOILHUMIDITY") {
      this.fetchSoilHistory();
    }
  },
};
</script>

<style scoped>
/* Styling for the component */
.sensor-details {
  padding: 20px;
  text-align: center;
}

.chart-container {
  margin: 20px auto;
  width: 80%;
  height: 400px;
  background: #f0f0f0;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

button {
  margin-top: 20px;
  background-color: #2d6d92;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #1e4e68;
}
</style>