<template>
  <div class="main">
    <el-container class="main-content">
      <el-collapse-transition>
        <el-aside :width="isCollapse ? '80px' : '210px'">
          <nav-menu :collapse="isCollapse" />
        </el-aside>
      </el-collapse-transition>
      <el-container class="page">
        <el-header class="page-header">
          <nav-header @foldChange="foldChange" :isCollapse="isCollapse" />
        </el-header>
        <el-main class="page-content">
          <!-- 页面视图 -->
          <div class="plr-10 page-content-main">
            <router-view></router-view>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { provide, ref } from 'vue';
import navHeader from './components/navHeader';
import navMenu from './components/navMenu';
const isCollapse = ref(false);
provide('isCollapse', isCollapse);
function foldChange() {
  isCollapse.value = !isCollapse.value;
}
</script>
<style scoped lang="scss">
.main {
  min-height: 100vh;

  .header {
    background-color: #fff;
  }

  .page-content {
    padding: 0;

    &-main {
      padding: 20px;
    }
  }
}
</style>
