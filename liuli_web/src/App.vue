<template>
  <el-config-provider :locale="locale">
    <router-view></router-view>
  </el-config-provider>
</template>

<script setup lang="ts">
import './style/common.scss';
import './style/global.scss';
import zhCn from 'element-plus/lib/locale/lang/zh-cn';
import { ElConfigProvider } from 'element-plus';
import en from 'element-plus/lib/locale/lang/en';

const locale = zhCn;

</script>

<style scoped lang="scss"></style>
