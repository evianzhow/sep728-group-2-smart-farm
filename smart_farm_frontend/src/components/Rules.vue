<template>
  <div class="rules-page">
    <h1>Automation Rules</h1>

    <!-- Add Rule Section -->
    <div class="add-rule">
      <h2>Add a Rule</h2>
      <form @submit.prevent="saveRule">
        <!-- Rule Name -->
        <!--
        <div class="form-group">
          <label for="ruleName">Rule Name:</label>
          <input
            id="ruleName"
            type="text"
            v-model="newRule.name"
            placeholder="Input Rule Name"
            required
          />
        </div> -->

        <!-- Trigger Sensor -->
        <div class="form-group">
          <label for="triggerSensor">Trigger Sensor:</label>
          <select id="triggerSensor" v-model="newRule.sensor" @change="updateSensor" required>
            <option value="" disabled>Select Sensor</option>
            <option value="SteamValue">Steam - Value</option>
            <option value="SteamPercentage">Steam - Percentage</option>
            <option value="DHT11Humidity">DHT11 - Humidity</option>
            <option value="DHT11TemperatureCelsius">DHT11 - Temperature(Celsius)</option>
            <option value="DHT11TemperatureFahrenhei">DHT11 - Temperature(Fahrenhei)</option>
            <option value="DHT11TemperatureKelvin">DHT11 - Temperature(Kelvin)</option>
            <option value="DHT11DewPointCelsius">DHT11 - DewPoint(Celsius)</option>
            <option value="SoilValue">Soil - Value</option>
            <option value="SoilPercentage">Soil - Percentage</option>
            <option value="WaterValue">Water - Value</option>
            <option value="WaterPercentage">Water - Percentage</option>
            <option value="UltrasonicDistance">Ultrasonic - Distance</option>
            <option value="LightValue">Light - Value</option>
            <option value="LightPercentage">Light - Percentage</option>
            <option value="Button">Button</option>
            <option value="PIR">PIR</option>
            <option value="Relay">Relay</option>
            <option value="LED">LED</option>
            <option value="Servo">Servo</option>
          </select>
        </div>

        <!-- Type -->
        <div class="form-group">
          <label for="type">Type:</label>
          <select id="type" v-model="newRule.type" required>
            <option value="" disabled>Select Type</option>
            <option value="threshold" :disabled="newRule.sensor === 'Button' || newRule.sensor === 'PIR' || newRule.sensor === 'Relay' || newRule.sensor === 'LED' || newRule.sensor === 'Servo'">Threshold</option>
            <option value="event" :disabled="newRule.sensor === 'SteamValue' || newRule.sensor === 'SteamPercentage' || newRule.sensor === 'DHT11Humidity' || newRule.sensor === 'DHT11TemperatureCelsius' || newRule.sensor === 'DHT11TemperatureFahrenhei' || newRule.sensor === 'DHT11TemperatureKelvin' || newRule.sensor === 'DHT11DewPointCelsius' || newRule.sensor === 'SoilValue' || newRule.sensor === 'SoilPercentage' || newRule.sensor === 'WaterValue' || newRule.sensor === 'WaterPercentage' || newRule.sensor === 'UltrasonicDistance' || newRule.sensor === 'LightValue' || newRule.sensor === 'LightPercentage'">Event</option>
          </select>
        </div>

        <!-- Operator and Value -->
        <div class="form-group">
          <label for="operator">Operator:</label>
          <select id="operator" v-model="newRule.operator" :disabled="!newRule.type" required>
            <option v-for="op in operators" :key="op" :value="op">{{ op }}</option>
          </select>
          <input id="thresholdValue" type="number" v-model="newRule.thresholdValue" :disabled="newRule.type === 'event'"
            placeholder="Input Threshold Value" />
        </div>

        <!-- Linked Controller -->
        <div class="form-group">
          <label for="linkedController">Linked Controller:</label>
          <select id="linkedController" v-model="newRule.controller" @change="updateActions" required>
            <option value="" disabled>Select Controller</option>
            <option value="OperateFan">Fan</option>
            <option value="OperateBuzzer">Buzzer</option>
            <option value="OperateRelay">Relay</option>
            <option value="OperateLED">LED</option>
            <option value="OperateServo">Servo</option>
            <option value="OperateLCD">LCD</option>
          </select>
        </div>
        <div class="form-group">
          <label for="linkedAction">Action:</label>
          <select id="linkedAction" v-model="newRule.action" required>
            <option value="" disabled>Select Action</option>
            <option v-for="action in actions" :key="action" :value="action">
              {{ action }}
            </option>
          </select>
        </div>

        <!-- Save and Cancel Buttons -->
        <div class="form-buttons">
          <button type="submit" class="save-btn">Save</button>
          <button type="button" class="cancel-btn" @click="resetForm">Cancel</button>
        </div>
      </form>
    </div>

    <!-- Existing Rules Section -->
    <div class="existing-rules">
      <h2>Existing Rules</h2>
      <table v-if="rules.length > 0">
        <thead>
          <tr>
            <th>Rule ID</th>
            <th>Trigger Sensor</th>
            <th>Type</th>
            <th>Operator</th>
            <th>Threshold</th>
            <th>Controller</th>
            <th>Action</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(rule, index) in rules" :key="index">
            <td>{{ rule.id }}</td>
            <td>{{ rule.trigger_sensor }}</td>
            <td>{{ rule.type }}</td>
            <td>{{ rule.op }}</td>
            <td>{{ rule.threshold }}</td>
            <td>{{ rule.target_controller }}</td>
            <td>{{ rule.action }}</td>
            <td>{{ new Date(rule.created_at).toLocaleTimeString([], {
              year: 'numeric', month: '2-digit', day: '2-digit',
              hour: '2-digit', minute: '2-digit', second: '2-digit' }) }}</td>
            <td> <button @click="deleteRule(index)">Delete</button> </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No rules found.</p>
    </div>


  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";
export default {
  name: "Rules",
  inject: ["getAuthToken"],
  data() {
    return {
      newRule: {
        name: "",
        sensor: "",
        type: "",
        operator: "",
        thresholdValue: null,
        controller: "",
        action: "",
      },
      types: ["threshold", "event"],
      rules: [], // Store existing rules
      actions: [], // Dynamically updated actions based on controller
      operators: [], // Dynamically updated operators based on sensor and type
    };
  },
  computed: {
  },
  methods: {
    mapSensorToTrigger(sensor) {
      const sensorMap = {
        SteamValue: "steam.value",
        SteamPercentage: "steam.percentage",
        DHT11Humidity: "dht11.humidity",
        DHT11TemperatureCelsius: "dht11.temperature.celsius",
        DHT11TemperatureFahrenhei: "dht11.temperature.fahrenheit",
        DHT11TemperatureKelvin: "dht11.temperature.kelvin",
        DHT11DewPointCelsius: "dht11.dewpoint.celsius",
        SoilValue: "soil.value",
        SoilPercentage: "soil.percentage",
        WaterValue: "water.value",
        WaterPercentage: "water.percentage",
        UltrasonicDistance: "ultrasonic.distance",
        LightValue: "light.value",
        LightPercentage: "light.percentage",
        Button: "button",
        PIR: "pir",
        Relay: "relay",
        LED: "led",
        Servo: "servo",
      };
      return sensorMap[sensor] || "unknown_sensor";
    },


    handleOperatorChange() {
      // Automatically set thresholdValue to null when 'event' is selected
      if (this.newRule.type === "event") {
        this.newRule.thresholdValue = null;
      }
    },

    mapActionOP(sensor, op) {
      const OPMap = {
        Button: {
          "Pressed": "pressed",
          "Released": "released",
        },
        PIR: {
          "Detected": "detected",
          "Not Detected": "not-detected",
        },
        Relay: {
          "Active(ON)": "active",
          "Active(OFF)": "inactive",
        },
        LED: {
          "Active(ON)": "active",
          "Active(OFF)": "inactive",
        },
        Servo: {
          "OPEN": "OPEN",
          "HALF_OPEN": "HALF_OPEN",
          "CLOSED": "CLOSED",
        },
      };

      // Check if the sensor exists in the OPMap
      if (OPMap[sensor]) {
        // Check if the op exists in the mapped sensor's operations
        return OPMap[sensor][op] || op; // Fallback to original `op` if no match
      }

      // If the sensor doesn't exist in OPMap, return the original `op`
      return op;
    },


    extractRuleData() {
      return {
        trigger_sensor: this.mapSensorToTrigger(this.newRule.sensor),
        type: this.newRule.type,
        op: this.mapActionOP(this.newRule.sensor, this.newRule.operator),
        threshold: this.newRule.thresholdValue ?? null,
        target_controller: this.mapControllerToTarget(this.newRule.controller),
        action: this.mapActionToTarget(
          this.newRule.controller,
          this.newRule.action
        ),
      };
    },

    mapControllerToTarget(controller) {
      const controllerMap = {
        OperateBuzzer: "buzzer",
        OperateFan: "fan",
        OperateServo: "servo",
        OperateRelay: "relay",
        OperateLED: "led",
      };

      return controllerMap[controller] || "unknown_controller"; // Fallback for unsupported controllers
    },


    mapActionToTarget(controller, action) {
      const actionMap = {
        OperateBuzzer: (action) => {
          const percentageMap = {
            "0S": "duration=0;frequency=6000",
            "5S": "duration=5000;frequency=6000",
            "10S": "duration=10000;frequency=6000",
            "30S": "duration=30000;frequency=6000",
          };
          return percentageMap[action] || {}; // Fallback if no match
        },
        OperateServo: (action) => {
          const percentageMap = {
            "OPEN": "position=OPEN",
            "HALF_OPEN": "position=HALF_OPEN",
            "CLOSED": "position=CLOSED",
          };
          return percentageMap[action] || {}; // Fallback if no match
        },
        OperateFan: (action) => {
          const percentageMap = {
            "0%": "speed=0",
            "25%": "speed=64",
            "50%": "speed=128",
            "75%": "speed=192",
            "100%": "speed=255",
          };
          return percentageMap[action] || {}; // Fallback if no match
        },
        OperateRelay: (action) => {
          const percentageMap = {
            "Active(ON)": "active=true",
            "Active(OFF)": "active=false"
          };
          return percentageMap[action] || {}; // Fallback if no match
        },
        OperateLED: (action) => {
          const percentageMap = {
            "Active(ON)": "active=true",
            "Active(OFF)": "active=false"
          };
          return percentageMap[action] || {}; // Fallback if no match
        },
        OperateLCD: (action) => {
          const percentageMap = {
            "5S": "duration=5000;message=Hello World",
            "10S": "duration=10000;message=Hello World",
          };
          return percentageMap[action] || {}; // Fallback if no match
        },

      };

      if (actionMap[controller]) {
        return actionMap[controller](action);
      } else {
        return "error"; // Fallback for unsupported controllers
      }
    },

    async saveRule() {
      const ruleData = this.extractRuleData();
      console.log("Rule Data to be saved:", JSON.stringify(ruleData, null, 2));

      try {
        const token = localStorage.getItem("authToken"); // Retrieve token from local storage
        const response = await axios.post(
          "https://gorgeous-glowworm-definite.ngrok-free.app/rules",
          ruleData,
          {
            headers: {
              Authorization: token, // Include token in the headers
            },
          }
        );
        console.log("Rule successfully saved:", response.data);

        alert("Rule saved successfully!");
        this.resetForm(); // Reset the form after saving
      } catch (error) {
        console.error("Error saving rule:", error);
        alert("Failed to save rule. Please try again.");
      }
    },


    async loadRules() {
      try {
        const token = localStorage.getItem("authToken"); // Retrieve the stored token
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/rules",
          {
            headers: {
              Authorization: token, // Include token in headers
            },
            params: {
              page: 1, // Default to the first page
              per_page: 25, // Default to 25 rules per page
            },
          }
        );

        // Assign the fetched rules to the data property
        this.rules = response.data.data;
        console.log("Loaded rules:", this.rules);
      } catch (error) {
        console.error("Error loading rules:", error);
      }
    },


    async deleteRule(index) {
      try {
        const token = localStorage.getItem("authToken"); // Retrieve the stored token
        const ruleId = this.rules[index].id; // Get the rule ID for the selected rule

        // Send DELETE request to the API
        await axios.delete(
          `https://gorgeous-glowworm-definite.ngrok-free.app/rules/${ruleId}`,
          {
            headers: {
              Authorization: token, // Include token in headers
            },
          }
        );

        // Remove the rule from the local list
        this.rules.splice(index, 1);

        alert(`Rule ID ${ruleId} deleted successfully.`);
        console.log(`Rule ID ${ruleId} deleted successfully.`);
      } catch (error) {
        console.error("Error deleting rule:", error);
        alert("Failed to delete the rule. Please try again.");
      }
    },

    updateActions(event) {
      // Dynamically update actions based on selected controller
      console.log("event.target.value:", event.target.value);
      switch (event.target.value) {
        case "OperateFan":
          this.actions = ["0%", "25%", "50%", "75%", "100%"];
          break;
        case "OperateBuzzer":
          this.actions = ["0S", "5S", "10S"];
          break;
        case "OperateRelay":
          this.actions = ["Active(ON)", "Inactive(OFF)"];
          break;
        case "OperateLED": // Both Relay and LED have the same actions
          this.actions = ["Active(ON)", "Inactive(OFF)"];
          break;
        case "OperateServo":
          this.actions = ["OPEN", "HALF_OPEN", "CLOSED"];
          break;
        case "OperateLCD":
          this.actions = ["5S", "10S"];
          break;
        default:
          this.actions = []; // Fallback for unknown controllers
      }
      this.newRule.action = ""; // Reset action when controller changes
    },

    updateOperator(sensorType) {
      if (sensorType === "threshold") {
        this.operators = [">=", "<=", "==", ">", "<", "!="]; // Threshold operators
      } else if (sensorType === "event") {
        switch (this.newRule.sensor) {
          case "Button":
            this.operators = ["Pressed", "Released"];
            break;
          case "PIR":
            this.operators = ["Detected", "Not Detected"];
            break;
          case "Relay":
          case "LED":
            this.operators = ["Active(ON)", "Active(OFF)"];
            break;
          case "Servo":
            this.operators = ["OPEN", "HALF_OPEN", "CLOSED"];
            break;
        }
      } else {
        this.operators = [];
      }
    },

    updateSensor(event) {
      console.log("event.target.value:", event.target.value);
      switch (event.target.value) {
        case "SteamValue":
        case "SteamPercentage":
        case "DHT11Humidity":
        case "DHT11TemperatureCelsius":
        case "DHT11TemperatureFahrenhei":
        case "DHT11TemperatureKelvin":
        case "DHT11DewPointCelsius":
        case "SoilValue":
        case "SoilPercentage":
        case "WaterValue":
        case "WaterPercentage":
        case "UltrasonicDistance":
        case "LightValue":
        case "LightPercentage":
          this.updateOperator("threshold");
          break;
        case "Button":
        case "PIR":
        case "Relay":
        case "LED":
        case "Servo":
          this.updateOperator("event");
          break;
      }
    },

    resetForm() {
      this.newRule = {
        sensor: "",
        operator: "",
        thresholdValue: null,
        controller: "",
        action: "",
      };
    },


  },
  mounted() {
    // Correct placement of mounted hook
    this.loadRules();
  },
};
</script>

<style scoped>
.rules-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

h1,
h2 {
  color: #2d6d92;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 5px;
}

input,
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

input:disabled,
select:disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
}

.form-buttons {
  display: flex;
  gap: 10px;
}

.save-btn {
  background-color: orange;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.save-btn:hover {
  background-color: darkorange;
}

.cancel-btn {
  background-color: purple;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.cancel-btn:hover {
  background-color: darkmagenta;
}

.existing-rules ul {
  list-style-type: none;
  padding: 0;
}

.existing-rules li {
  background-color: #f9f9f9;
  margin: 5px 0;
  padding: 10px;
  border-radius: 4px;
}
</style>
