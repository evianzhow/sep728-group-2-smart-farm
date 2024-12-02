<template>
    <div class="pir-details">
      <h1>PIR Sensor Details</h1>
      <table v-if="history.length > 0">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Detected State</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in history" :key="index">
            <td>{{ item.timestamp }}</td>
            <td>{{ item.value ? "Detected" : "Not Detected" }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No history available.</p>
      <button @click="goHome">Back to Home</button>
    </div>
</template>

<script>
import axios from "axios";

export default {
  inject: ["getAuthToken"],
  name: "PIRDetails",
  data() {
    return {
      history: [], // To store the PIR history data
    };
  },
  methods: {
    async fetchPIRHistory() {
      try {
        const token = await this.getAuthToken(); // Ensure you have a valid token
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/pir/history",
          {
            headers: { Authorization: token },
            params: {
              page: 1,
              per_page: 25,
              start_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // Last 24 hours
              end_time: new Date().toISOString(),
            },
          }
        );

        console.log("PIR History Response:", response.data.data);

        // Assign the fetched data to the history array
        this.history = response.data.data.map((entry) => ({
          value: entry.value,
          timestamp: new Date(entry.timestamp).toLocaleString(), // Format timestamp
        }));
      } catch (error) {
        console.error("Error fetching PIR history:", error);
      }
    },
    goHome() {
      this.$router.push("/home"); // Navigate back to the Home page
    },
    getAuthToken() {
      return localStorage.getItem("authToken"); // Retrieve token from localStorage
    },
  },
  mounted() {
    this.fetchPIRHistory(); // Fetch PIR history data when the component mounts
  },
};
</script>

<style scoped>
.pir-details {
  margin: 20px;
  font-family: Arial, sans-serif;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th, td {
  border: 1px solid #ddd;
  text-align: left;
  padding: 8px;
}

th {
  background-color: #f4f4f4;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

button:hover {
  background-color: #0056b3;
}
</style>
