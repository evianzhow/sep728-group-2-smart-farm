<template>
  <div class="button-container">
    <h1>Settings</h1>
    <button @click="checkUpdate" style="margin: 10px; padding: 10px 20px;">Check Update</button>
    <button @click="clearStorage" style="margin: 10px; padding: 10px 20px; background-color: red; color: white;">Clear Storage</button>
    <button @click="logout" style="margin: 10px; padding: 10px 20px; background-color: #007bff; color: white;">Logout</button>
    <p style="font-size: 12px; color: gray;">Version 1.0</p>
  </div>
</template>


<script>
/* eslint-disable */
import axios from 'axios';

export default {
  name: "SettingsPage",
  inject: ["getAuthToken"],
  data() {
    return {
      showWarning: false, // Flag to control the visibility of the warning message
    };
  },
  methods: {
    checkUpdate() {
      this.showWarning = true; // Show the warning message when button is clicked
    },
    clearStorage() {
      localStorage.clear();
      console.log("Storage cleared");
      this.$router.push('/login');
    },
    async logout() {
      const token = await this.getAuthToken();

      try {
        await axios.post(
          "https://gorgeous-glowworm-definite.ngrok-free.app/logout",
          {
            headers: {
              Authorization: token,
            },
          }
        );
        console.log(`Logout successful!`);
        localStorage.clear();
        console.log("Storage cleared");
        this.$router.push('/login');
      } catch (error) {
        console.error("Failed to logout:", error);
      }
    }
  },
};
</script>

<style scoped>
/* Add any additional styles here */
.button-container {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
</style>
