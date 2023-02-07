<template>
  <div class="app-content bg-white">
    <p>{{ title }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const title = ref('日志管理');
</script>

<style></style>
