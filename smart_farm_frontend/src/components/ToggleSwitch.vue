<template>
  <div class="toggle-switch">
    <h3>{{ label }}</h3>
    <button class="trigger-button" @click="toggleDevice">Trigger</button>
  </div>
</template>

  
  <script>
  import axios from "axios";
  
  export default {
    inject: ["getAuthToken", "apiEndpoint"],
    name: "ToggleSwitch",
    props: {
      label: {
        type: String,
        required: true,
      },
    },
    data() {},
    methods: {
      async toggleDevice() {
      const token = await this.getAuthToken();
      const now = new Date().toISOString();

      let endpoint = "";
      let params = {};

      // Define logic based on the label
      switch (this.label) {
        case "Passive Buzzer":
          endpoint = "/controllers/buzzer";
          params = { active: true, frequency: 6000, duration: 1000, timestamp: now };
          break;

        // Add more devices here
        case "LCD":
            endpoint = "/controllers/lcd";
            params = { message: "Hello World!", duration: 10000, timestamp: now };
            break;

        default:
          console.error(`Unknown device: ${this.label}`);
          return;
      }

      // Make the API request
      try {
        await axios.post(
          `${this.apiEndpoint}/${endpoint}`,
          params,
          {
            headers: {
              Authorization: token,
            },
          }
        );
        console.log(`${this.label} successfully to turn on`);
      } catch (error) {
        console.error(`Failed to control ${this.label}:`, error);
      }
    },

    },
  };
  </script>
  
  <style scoped>
.toggle-switch {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f9fafc; /* Light background */
  border: 1px solid #dcdfe6; /* Subtle border */
  border-radius: 10px; /* Rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Shadow for depth */
  padding: 20px; /* Padding inside the box */
  width: 200px; /* Fixed width for consistent size */
  margin: 10px; /* Space around each toggle switch */
  text-align: center;
}

.toggle-switch h3 {
  font-size: 1.2em; /* Slightly larger title */
  font-weight: bold;
  color: #333; /* Darker text color */
  margin-bottom: 15px; /* Space below the title */
}

.trigger-button {
  padding: 10px 20px; /* Padding inside the button */
  background-color: #007bff; /* Blue background for buttons */
  color: white; /* White text color */
  border: none; /* Remove border */
  border-radius: 5px; /* Rounded button corners */
  cursor: pointer; /* Pointer cursor on hover */
  font-size: 16px; /* Font size for button text */
  transition: background-color 0.3s, transform 0.2s; /* Smooth transitions */
}

.trigger-button:hover {
  background-color: #0056b3; /* Darker blue on hover */
  transform: translateY(-2px); /* Slight lift effect */
}

.trigger-button:active {
  background-color: #003f7f; /* Even darker blue on click */
  transform: translateY(0); /* Reset lift on click */
}
</style>

  
  