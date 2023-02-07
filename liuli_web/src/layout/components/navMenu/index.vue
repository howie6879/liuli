<template>
  <div class="nav-menu">
    <div class="logo plr-20 flex f-ac-jc">
      <img
        class="img"
        :style="collapse ? 'height:40px' : 'height:50px'"
        src="~@/assets/images/logo.png"
        alt="logo"
      />
      <transition>
        <span v-show="!collapse" class="title ml-10">琉璃后台</span>
      </transition>
    </div>
    <el-menu
      :default-active="currentItemId"
      class="el-menu-vertical"
      background-color="#FFF"
      :collapse="collapse"
      text-color="#000"
      active-text-color="#0a60bd"
      @open="openMenu"
      collapse-transition
    >
      <template v-for="(item, index) in menuList" :key="item.name">
        <!-- <menuItem :data="item" base-path="/" :index="index">
                    </menuItem> -->
        <AppLink :to="resolvePath(item.path, '/')">
          <el-menu-item :index="resolvePath(item.path, '/')">
            <item v-bind="item.meta"></item>
          </el-menu-item>
        </AppLink>
        <template v-if="index === 3">
          <hr class="line" />
        </template>
      </template>
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { routes } from '@/router';
import AppLink from '../AppLink';
import item from './item';
import { resolvePath } from '@/utils';

const props = defineProps({
  collapse: {
    type: Boolean,
    default: false
  }
});

const route = useRoute();
const router = useRouter();

// 筛选出一级菜单
const menuList = computed(() => {
  const list = routes.find((item) => item.path === '/');
  return list.children ?? [];
});

// 高亮的index
const currentItemId = computed(() => {
  const { path } = route;
  return path;
});

// 展开菜单时自动跳转
function openMenu(index, indexPath) {
  let path = indexPath[indexPath.length - 1];
  router.push(path);
}
</script>

<style scoped lang="scss">
.nav-menu {
  height: calc(100vh - 20px);
  background-color: #fff;

  .logo {
    height: 60px;

    .img {
      // height: 50px;
      margin: 0 10px;
    }

    .title {
      font-size: 16px;
      font-weight: 700;
      color: #000;
    }
  }

  // 目录
  .el-submenu {
    background-color: #fff !important;

    // 二级菜单 ( 默认背景 )
    .el-menu-item {
      padding-left: 50px !important;
      background-color: #fff !important;
    }
  }

  :deep(.el-submenu__title) {
    background-color: #fff !important;
  }

  // hover 高亮
  .el-menu-item:hover {
    color: #fff !important; // 菜单
  }

  .el-menu-item.is-active {
    // color: #fff !important;
    // background-color: #0a60bd !important;
  }

  .line {
    background-color: rgba(0, 0, 0, 0.1);
    height: 2px;
  }
}
</style>
