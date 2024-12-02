<template>
  <div class="range-slider">
    <h3>{{ label }}</h3>
    <div class="switch-container" @click="toggleFan">
      <div class="toggle-button" :class="{ on: isOn }"></div>
      <span>{{ isOn ? "ON" : "OFF" }}</span>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  inject: ["getAuthToken"],
  name: "RangeSlider",
  props: {
    label: {
      type: String,
      default: "Fan",
    },
  },
  data() {
    return {
      isOn: false, // Default state is OFF
      fanSpeed: 140, // Default speed when ON
    };
  },
  methods: {
    async toggleFan() {
      const token = await this.getAuthToken();
      const payload = {
        speed: this.isOn ? 0 : this.fanSpeed, // 0 for OFF, fanSpeed for ON
      };

      try {
        const response = await axios.post(
          "https://gorgeous-glowworm-definite.ngrok-free.app/controllers/fan",
          payload,
          {
            headers: {
              Authorization: token,
            },
          }
        );
        console.log(`Fan ${this.isOn ? "turned off" : "turned on"} successfully`, response.data);
      } catch (error) {
        console.error(`Error ${this.isOn ? "turning off" : "turning on"} the fan:`, error);
      }

      // Toggle the switch state
      this.isOn = !this.isOn;
    },
  },
};
</script>

<style scoped>
.range-slider {
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
