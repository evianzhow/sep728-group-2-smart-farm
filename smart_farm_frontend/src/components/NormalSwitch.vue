<template>
  <div class="toggle-switch">
    <h3>{{ label }}</h3>
    <div class="switch-container" @click="toggleDevice">
      <div class="toggle-button" :class="{ on: isOn }"></div>
      <span>{{ isOn ? 'ON' : 'OFF' }}</span>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  inject: ["getAuthToken"],
  name: "ToggleSwitch",
  props: {
    label: {
      type: String,
      required: true, // The device type, e.g., "LED", "Relay Module"
    },
  },
  data() {
    return {
      intervalId: null,
      isOn: false, // Default state is OFF
    };
  },
  methods: {
    async toggleDevice() {
      const token = await this.getAuthToken();
      const now = new Date().toISOString();

      const params = this.isOn
        ? {
          active: false,
          timestamp: now,
        }
        : {
          active: true,
          timestamp: now,
        };

      // Determine API endpoint based on the label
      let endpoint = "";
      if (this.label === "LED") {
        endpoint = "https://gorgeous-glowworm-definite.ngrok-free.app/controllers/led";
      } else if (this.label === "Relay Module") {
        endpoint = "https://gorgeous-glowworm-definite.ngrok-free.app/controllers/relay";
      } else {
        console.error("Unknown device type:", this.label);
        return;
      }

      try {
        await axios.post(endpoint, params, {
          headers: {
            Authorization: token,
          },
        });
        console.log(`${this.label} is now ${this.isOn ? "OFF" : "ON"}`);
        this.isOn = !this.isOn; // Toggle the state
      } catch (error) {
        console.error(`Failed to toggle ${this.label}:`, error);
      }
    },
    async fetchData() {
      const token = await this.getAuthToken();
      let endpoint = "";
      if (this.label === "LED") {
        endpoint = `https://gorgeous-glowworm-definite.ngrok-free.app/controllers/led/preview`;
      } else if (this.label === "Relay Module") {
        endpoint = `https://gorgeous-glowworm-definite.ngrok-free.app/controllers/relay/preview`;
      }
      if (endpoint) {
        const response = await axios.get(endpoint, {
          headers: {
            Authorization: token,
          },
        });
        this.isOn = response.data.active;
      }
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
.toggle-switch {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f9fafc;
  border: 1px solid #dcdfe6;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 200px;
  margin: 10px;
  text-align: center;
}

.toggle-button {
  width: 50px;
  height: 25px;
  background-color: #ccc;
  border-radius: 15px;
  position: relative;
  transition: all 0.3s;
  margin-bottom: 10px;
}

.toggle-button.on {
  background-color: #007bff;
}

.toggle-button::after {
  content: "";
  position: absolute;
  top: 2px;
  left: 2px;
  width: 21px;
  height: 21px;
  background-color: white;
  border-radius: 50%;
  transition: all 0.3s;
}

.toggle-button.on::after {
  left: calc(100% - 23px);
}

.switch-container {
  cursor: pointer;
}

h3 {
  font-size: 1.2em;
  margin-bottom: 10px;
}

span {
  font-size: 1em;
  color: #333;
}
</style>
