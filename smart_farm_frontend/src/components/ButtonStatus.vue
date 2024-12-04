<template>
  <div class="button-status">
    <h3>{{ label }}</h3>
    <div class="status-container">
      <span>{{ new Date(lastUpdatedTime).toLocaleString([], { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' }) }}</span>
      <span>{{ status }}</span>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ButtonStatus",
  props: {
    label: {
      type: String,
      required: true, // Ensure that label is provided
    },
  },
  inject: ["getAuthToken"],
  data() {
    return {
      intervalId: null, // Add this to store the interval ID
      lastUpdatedTime: null,
      stateMap: {
        Button: ["Pressed", "Released"], // States for Button
        PIR: ["Activated", "Inactivated"], // States for PIR
      },
      currentIndex: 0, // Default index for the first state
    };
  },
  computed: {
    // Determine the states dynamically based on the label
    states() {
      return this.stateMap[this.label] || ["Unknown", "Unknown"]; // Fallback to "Unknown" if no matching label
    },
    // Display the current state
    status() {
      return this.states[this.currentIndex];
    },
  },
  methods: {
    // Fetch data dynamically based on label
    async fetchData() {
      try {
        const token = await this.getAuthToken();
        console.log("Token being used:", token);

        let endpoint = "";
        if (this.label === "PIR") {
          endpoint = "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/pir/preview";
        } else if (this.label === "Button") {
          endpoint = "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/button/preview";
        }

        if (endpoint) {
          const response = await axios.get(endpoint, {
            headers: {
              Authorization: token,
            },
          });
          console.log("Response data for", this.label, ":", response.data);

          // Update the current index based on the response
          if (this.label === "PIR") {
            this.currentIndex =
              response.data.value === "inactivated" || response.data.value === false
                ? 1
                : 0; // Activated/Inactivated
          } else if (this.label === "Button") {
            this.currentIndex =
              response.data.pressed === "releaseds" || response.data.pressed === false
                ? 1
                : 0; // Pressed/Released
          }
          // response.data.timestamp is should like "2024-12-03T21:46:18.000Z"
          this.lastUpdatedTime = new Date(response.data.timestamp).toLocaleTimeString();
        } else {
          console.error("No endpoint configured for label:", this.label);
        }
      } catch (error) {
        console.error("Error fetching data for", this.label, ":", error);
      }
    },
  },
  mounted() {
    // Fetch data every 5 seconds
    this.intervalId = setInterval(() => {
      this.fetchData();
    }, 5000);
  },
  unmounted() {
    // Clear the interval when the component is unmounted
    clearInterval(this.intervalId);
  },
};
</script>

<style scoped>
.button-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #2d6d92; /* Background color */
  color: white;
  border-radius: 8px;
  padding: 20px;
  width: 150px;
  height: 150px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.status-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
}

.status-container span:last-child {
  text-transform: uppercase; /* Display state in uppercase */
  font-weight: bold;
  margin-top: 10px;
}
</style>
