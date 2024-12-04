<template>
  <div class="cata-slider">
    <h3>{{ label }}</h3>
    <div class="slider-container">
      <button v-for="(state, index) in states" :key="state" :class="{ active: currentIndex === index }"
        @click="setServoState(index)">
        {{ state }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  inject: ["getAuthToken"],
  name: "CataSlider",
  props: {
    label: {
      type: String,
      default: "Servo",
    },
  },
  data() {
    return {
      intervalId: null,
      states: ["OPEN", "HALF_OPEN", "CLOSED"], // Available states
      currentIndex: 0, // Default state is "OPEN"
    };
  },
  methods: {
    async setServoState(index) {
      const token = await this.getAuthToken();
      const now = new Date().toISOString();

      // Map index to the corresponding state
      const state = this.states[index];

      const params = {
        position: state,
        timestamp: now,
      };

      try {
        await axios.post(
          "https://gorgeous-glowworm-definite.ngrok-free.app/controllers/servo",
          params,
          {
            headers: {
              Authorization: token,
            },
          }
        );
        console.log(`Servo set to ${state}`);
        this.currentIndex = index; // Update current state index
      } catch (error) {
        console.error("Failed to set servo state:", error);
      }
    },
    async fetchData() {
      const stateMapping = {
        "OPEN": 0,
        "HALF_OPEN": 1,
        "CLOSED": 2,
      };
      const token = await this.getAuthToken();
      const response = await axios.get("https://gorgeous-glowworm-definite.ngrok-free.app/controllers/servo/preview", {
        headers: {
          Authorization: token,
        },
      });
      this.currentIndex = stateMapping[response.data.position] || 0;
    },
  },
  async mounted() {
    this.intervalId = setInterval(() => {
      this.fetchData();
    }, 5000);
  },
  unmounted() {
    clearInterval(this.intervalId);
  },
};
</script>

<style scoped>
.cata-slider {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f9fafc;
  border: 1px solid #dcdfe6;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 25px;
  /* Increased padding for a larger frame */
  width: 250px;
  /* Increased width */
  height: 90px;
  /* Increased height */
  text-align: center;
  margin: 15px;
}

.cata-slider h3 {
  font-size: 1.2em;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.slider-container {
  display: flex;
  /* Inline buttons */
  justify-content: space-between;
  /* Spacing between buttons */
  align-items: center;
  width: 100%;
  /* Ensure buttons fill the width of the frame */
  margin-top: 10px;
}

.slider-container button {
  flex: 1;
  /* Ensure buttons have equal width */
  margin: 0 5px;
  padding: 5px 10px;
  /* Keep buttons compact */
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  /* Compact font size */
  transition: background-color 0.3s, transform 0.2s;
}

.slider-container button.active {
  background-color: #0056b3;
}

.slider-container button:hover {
  background-color: #0056b3;
  transform: scale(1.05);
  /* Slight enlargement on hover */
}

.slider-container button:active {
  transform: scale(1);
}
</style>
