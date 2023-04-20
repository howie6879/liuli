<template>
  <div class="main">
    <el-container class="main-content">
      <el-collapse-transition>
        <el-aside :width="isCollapse ? '80px' : '245px'">
          <nav-menu :collapse="isCollapse" />
        </el-aside>
      </el-collapse-transition>
      <el-container class="page">
        <el-header class="page-header">
          <nav-header @foldChange="foldChange" :isCollapse="isCollapse" />
        </el-header>
        <el-scrollbar>
          <el-main class="page-content">
            <!-- 页面视图 -->
            <div class="page-content-main">
              <router-view></router-view>
            </div>
          </el-main>
        </el-scrollbar>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { provide, ref } from 'vue';
import navHeader from "./components/navHeader/index.vue"
import navMenu from './components/navMenu/index.vue';
const isCollapse = ref(false);
provide('isCollapse', isCollapse);
function foldChange() {
  isCollapse.value = !isCollapse.value;
}
</script>
<style scoped lang="scss">
.main {
  min-height: 100vh;

  .el-aside {
    transition: all 0.4s ease-in-out;
  }

  .page-content {
    padding: 0;
    min-width: 1080px;
    height: auto;
    overflow: auto;

    &-main {
      padding: 20px;
    }
  }
}
</style>
