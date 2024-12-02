<template>
  <div style="text-align: center; margin-top: 20px;">
    <h1>Settings</h1>
    <button @click="checkUpdate" style="margin: 10px; padding: 10px 20px;">Check Update</button>
    <p v-if="showWarning" style="color: red;">This is the newest version.</p>
    <p style="font-size: 12px; color: gray;">Version 1.0</p>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "SettingsPage",
  data() {
    return {
      showWarning: false, // Flag to control the visibility of the warning message
    };
  },
  methods: {
    checkUpdate() {
      this.showWarning = true; // Show the warning message when button is clicked
    },
  },
};
</script>

<style scoped>
/* Add any additional styles here */
</style>
