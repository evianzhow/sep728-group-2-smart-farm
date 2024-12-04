<template>
    <div class="relay-details">
      <h1>Relay Details</h1>
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
  name: "RelayDetails",
  inject: ["getAuthToken", "apiEndpoint"],
  data() {
    return {
      history: [], // To store the relay history data
    };
  },
  methods: {
    async fetchRelayHistory() {
      try {
        const token = await this.getAuthToken(); // Ensure you have a valid token
        const response = await axios.get(
          `${this.apiEndpoint}/controllers/relay/history`,
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

        console.log("Relay History Response:", response.data.data);

        // Assign the fetched data to the history array
        this.history = response.data.data.map((entry) => ({
          active: entry.active,
          timestamp: new Date(entry.timestamp).toLocaleString(), // Format timestamp
        }));
      } catch (error) {
        console.error("Error fetching relay history:", error);
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
    this.fetchRelayHistory(); // Fetch relay history data when the component mounts
  },
};
</script>

<style scoped>
.relay-details {
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

