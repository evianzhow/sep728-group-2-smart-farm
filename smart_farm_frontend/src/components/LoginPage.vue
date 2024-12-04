<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h2>Login</h2>

      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="credentials.username" required>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="credentials.password" required>
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>

      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginPage',
  inject: ["getAuthToken", "apiEndpoint"],
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      loading: false,
      error: null
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post(`${this.apiEndpoint}/login`, this.credentials);

        // Assuming the API returns a token
        const token = response.data.token;

        // Store the token in localStorage or Vuex store
        localStorage.setItem('authToken', token);

        this.getAuthToken();
        // Redirect to home page
        this.$router.push('/home');
      } catch (err) {
        this.error = err.response?.data?.message || 'Login failed. Please try again.';
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.credentials.username = "admin";
    this.credentials.password = "securepassword";
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #ff0000;
  margin-top: 1rem;
  text-align: center;
}
</style>
