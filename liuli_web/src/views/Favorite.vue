<template>
  <SideBar @menuStatus="menuStatus" />
  <div class="content" :class="{ collapsed: collapsed }">
    <Header :title="title" />
    <main class="main-content">
      <p>Home</p>
    </main>
  </div>
</template>

<script setup>
import Header from '../components/Header.vue';
import SideBar from '../components/SideBar.vue';

import { onMounted, ref } from 'vue';
import { useUserStore } from '../store/user';

const collapsed = ref(false);
const title = ref('我的收藏');

function menuStatus(value) {
  // 获取导航栏传递过来的状态值
  collapsed.value = value;
}

onMounted(() => {
  const userStore = useUserStore();
  // console.log(userStore.getToken);
});
</script>

<style></style>
