<template>
  <el-icon>
    <svg-icon :name="icon" :prefix="`icon`"></svg-icon>
  </el-icon>
  <span v-show="!isCollapse">{{ title }}</span>
</template>
<script setup lang="ts">
import { inject } from '@vue/runtime-core';

const isCollapse = inject('isCollapse', false);
const props = defineProps({
  icon: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: ''
  }
});
</script>
