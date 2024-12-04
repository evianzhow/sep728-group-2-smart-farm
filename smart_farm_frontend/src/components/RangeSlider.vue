<template>
  <div class="range-slider">
    <h3>{{ label }}</h3>
    <div class="slider-container">
      <div class="slider-steps">
        <div 
          v-for="step in steps" 
          :key="step.value"
          class="step-button"
          :class="{ active: currentStep === step.value }"
          @click="setFanSpeed(step.value)"
        >
          {{ step.label }}
        </div>
      </div>
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
      currentStep: 0,
      steps: [
        { value: 0, label: '0%', speed: 0 },
        { value: 1, label: '25%', speed: 64 },
        { value: 2, label: '50%', speed: 128 },
        { value: 3, label: '75%', speed: 192 },
        { value: 4, label: '100%', speed: 255 },
      ],
    };
  },
  methods: {
    async setFanSpeed(step) {
      const token = await this.getAuthToken();
      const selectedStep = this.steps[step];
      const payload = {
        speed: selectedStep.speed,
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
        console.log(`Fan speed set to ${selectedStep.label}`, response.data);
        this.currentStep = step;
      } catch (error) {
        console.error(`Error setting fan speed:`, error);
      }
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

.slider-container {
  width: 100%;
  padding: 10px;
}

.slider-steps {
  display: flex;
  justify-content: space-between;
  gap: 5px;
}

.step-button {
  padding: 8px;
  background-color: #f0f0f0;
  border-radius: 5px;
  cursor: pointer;
  flex: 1;
  text-align: center;
  transition: all 0.3s;
}

.step-button:hover {
  background-color: #e0e0e0;
}

.step-button.active {
  background-color: #007bff;
  color: white;
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
