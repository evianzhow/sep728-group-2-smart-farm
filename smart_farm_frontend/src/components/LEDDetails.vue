
<template>
    <div class="led-details">
      <h1>LED Details</h1>
      <table v-if="history.length > 0">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in history" :key="index">
            <td>{{ item.timestamp }}</td>
            <td>{{ item.active ? "Active" : "Inactive" }}</td>
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
  name: "LEDDetails",
  inject: ["getAuthToken"],
  data() {
    return {
      history: [], // To store the LED history data
    };
  },
  methods: {
    async fetchLEDHistory() {
      try {
        const token = await this.getAuthToken(); // Ensure you have a valid token
        const response = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/controllers/led/history",
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

        console.log("LED History Response:", response.data.data);

        // Assign the fetched data to the history array
        this.history = response.data.data.map((entry) => ({
          active: entry.active,
          timestamp: new Date(entry.timestamp).toLocaleString(), // Format timestamp
        }));
      } catch (error) {
        console.error("Error fetching LED history:", error);
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
    this.fetchLEDHistory(); // Fetch LED history data when the component mounts
  },
};
</script>

<style scoped>
.led-details {
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
