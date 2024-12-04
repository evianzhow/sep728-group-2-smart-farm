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

export default {
  name: "App",
  data() {
    return {
      authToken: "", 
    };
  },
  methods: {
    getAuthToken() {
      const storedToken = localStorage.getItem("authToken");
      if (!storedToken) {
        this.$router.push('/login');
        return null;
      }
      if (storedToken && this.authToken !== storedToken) {
        this.authToken = storedToken;
      }
      return this.authToken;
    },
  },
  provide() {
    return {
      getAuthToken: this.getAuthToken,
    };
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
