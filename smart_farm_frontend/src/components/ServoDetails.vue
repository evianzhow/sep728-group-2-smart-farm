<template>
    <div class="servo-details">
      <h1>Servo Details</h1>
      <table v-if="history.length > 0">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Position</th>
            <th>Angle</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in history" :key="index">
            <td>{{ item.timestamp }}</td>
            <td>{{ item.position || "N/A" }}</td>
            <td>{{ item.angle !== null ? item.angle + "°" : "N/A" }}</td>
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
  name: "ServoDetails",
  data() {
    return {
      history: [], // To store the servo history data
    };
  },
  methods: {
    async fetchServoHistory() {
      try {
        const token = await this.getAuthToken(); // Ensure you have a valid token
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/controllers/servo/history",
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

        console.log("Servo History Response:", response.data.data);

        // Assign the fetched data to the history array
        this.history = response.data.data.map((entry) => ({
          position: entry.position || null,
          angle: entry.angle || null,
          timestamp: new Date(entry.timestamp).toLocaleString(), // Format timestamp
        }));
      } catch (error) {
        console.error("Error fetching servo history:", error);
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
    this.fetchServoHistory(); // Fetch servo history data when the component mounts
  },
};
</script>

<style scoped>
.servo-details {
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
