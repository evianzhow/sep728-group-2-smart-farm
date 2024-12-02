<!-- cd smart_farm_frontend-->
<!-- npm run serve -->
<!---& "C:\Program Files\Google\Chrome\Application\chrome.exe" --disable-web-security --user-data-dir="C:\chrome-dev-disabled-cors"-->
<template>
  <div id="app">
    
    <div class="sidebar">
      <router-link to="/home">Home</router-link>
      <router-link to="/rules">Rules</router-link>
      <router-link to="/settings">Settings</router-link>
    </div>
    
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      authToken: "", 
    };
  },
  methods: {
    
    async fetchAuthToken() {
      try {
        const response = await axios.post(
          "https://gorgeous-glowworm-definite.ngrok-free.app/login",
          {
            username: "admin", // Fixed username
            password: "securepassword", // Fixed password
          }
        );
        this.authToken = response.data.token; // Store the new token
        console.log("Token fetched:", this.authToken);
        localStorage.setItem("authToken", this.authToken); // Save the token to localStorage
      } catch (error) {
        console.error("Failed to fetch token:", error);
        this.authToken = null; // Reset the token if fetching fails
        throw error; // Propagate the error to the caller
      }
    },
    
    async getAuthToken() {
        const storedToken = localStorage.getItem("authToken");
      if (this.authToken) {
        // If the token is already in memory, return it
        console.log("Token already in memory:", this.authToken);
        return this.authToken;
      }
      if (storedToken) {
        // If a token exists in localStorage, use it
        console.log("Token loaded from localStorage:", storedToken);
        this.authToken = storedToken;
        return storedToken;
      } else {
        // If no token exists, fetch a new one
        console.log("No stored token found, fetching a new one...");
        await this.fetchAuthToken();
        return this.authToken;
      }
    },
    
    async refreshAuthTokenIfNeeded() {
      if (!this.authToken) {
        // If no token is available, fetch a new one
        console.log("No token in memory, fetching a new one...");
        await this.fetchAuthToken();
        return;
      }

      try {
        // Validate the token by making a test API call
        const testResponse = await axios.get(
          "https://gorgeous-glowworm-definite.ngrok-free.app/sensors/light/preview",
          {
            headers: {
              Authorization: this.authToken,
            },
          }
        );
        console.log("Token is valid:", testResponse.data);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // If the token is invalid, fetch a new one
          console.log("Token expired, fetching a new one...");
          await this.fetchAuthToken();
        } else {
          console.error("Unexpected error when validating token:", error);
        }
      }
    },
  },
  provide() {
    return {
      getAuthToken: async () => {
        await this.refreshAuthTokenIfNeeded(); // Ensure the token is valid
        return this.authToken; // Return the valid token
      },
    };
  },
  async mounted() {
    try {
      const storedToken = localStorage.getItem("authToken");
      if (storedToken) {
        // Load the token from localStorage if available
        console.log("Token loaded from localStorage:", storedToken);
        this.authToken = storedToken;

        // Validate the loaded token
        await this.refreshAuthTokenIfNeeded();
      } else {
        // Fetch a new token if none is stored
        console.log("No stored token found, fetching a new one...");
        await this.fetchAuthToken();
      }
    } catch (error) {
      console.error("Error during initialization:", error);
    }
  },
};
</script>

<style scoped>

#app {
  display: flex;
  height: 100vh;
}

.sidebar {
  background-color: #f4f4f4;
  padding: 20px;
  width: 200px;
  display: flex;
  flex-direction: column;
}

.sidebar a {
  text-decoration: none;
  color: white;
  background-color: #4caf50;
  padding: 10px 15px;
  margin: 5px 0;
  text-align: center;
  border-radius: 5px;
}

.sidebar a:hover {
  background-color: #45a049;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
