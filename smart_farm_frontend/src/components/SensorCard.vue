<template>
    <div class="sensor-card" :style="{ borderColor: color }">
      <div class="header">
        <span>{{ title }}</span>
        <span class="icon">{{ icon }}</span>
      </div>
      <div class="value">
        {{ value }}
      </div>
    </div>
</template>
  
<script>
  export default {
    name: "SensorCard",
    props: {
      title: {
        type: String,
        required: true,
      },
      value: {
        type: String,
        required: true,
      },
      icon: {
        type: String,
        required: true,
      },
      color: {
        type: String,
        required: true,
      },
    },
  };
</script>
  
<style scoped>
  .sensor-card {
    width: 275px;
    height: 150px;
    background-color: #fff;
    border: 2px solid;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    padding: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    width: 100%;
    font-weight: bold;
    color: #555;
  }
  
  .icon {
    font-size: 20px;
  }
  
  .value {
    font-size: 24px;
    font-weight: bold;
    color: #333;
  }
</style>
  