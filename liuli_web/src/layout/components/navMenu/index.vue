<template>
  <div class="nav-menu">
    <!-- 头部 -->
    <div class="logo flex justify-center items-center flex-shrink-0">
      <a class="font-bold text-[18px] text-textColor" href="https://github.com/liuli-io/liuli" target="_blank">LIULI</a>
    </div>
    <!-- 菜单 -->
    <el-scrollbar>
      <hr class="line" />
      <el-menu :default-active="currentItemId" class="el-menu-vertical" background-color="#FFF" :collapse="collapse"
        :collapse-transition="false" :unique-opened="false" text-color="#41454D" active-text-color="#41454D"
        @open="openMenu">
        <template v-for="(item, index) in menuList" :key="item.name">
          <!-- <menuItem :data="item" base-path="/" :index="index">
                    </menuItem> -->
          <AppLink :to="resolvePath(item.path, '/')">
            <el-menu-item :index="resolvePath(item.path, '/')" :class="[!collapse ? 'big-menu-item' : 'small-menu-item']">
              <menuItem v-bind="item.meta">
              </menuItem>
            </el-menu-item>
          </AppLink>
          <template v-if="index === 3">
            <hr class="line" />
            <div class="text-[#a6aab2] text-[14px] ml-4 mt-3 whitespace-nowrap" v-show="!collapse">
              我的设置
            </div>
          </template>
        </template>
      </el-menu>
    </el-scrollbar>
    <!-- 版本 -->
    <!-- <div class="text-[13px] text-textColor text-center">v 1.1.1</div> -->
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { routes } from '@/router';
import AppLink from '../appLink.vue';
import menuItem from './menuItem.vue'
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
  return list!.children ?? [];
});

// 高亮的index
const currentItemId = computed(() => {
  const { path } = route;
  return path;
});

// 展开菜单时自动跳转
function openMenu(index: any, indexPath: string | any[]) {
  let path = indexPath[indexPath.length - 1];
  router.push(path);
}
</script>

<style scoped lang="scss">
.nav-menu {
  box-sizing: border-box;
  padding: 0 6px;
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #fff;
  transition: all 0.3s ease;

  .logo {
    height: 60px;
    margin: 0 auto;
  }

  // 目录
  .el-submenu {
    background-color: #fff !important;

    // 二级菜单 ( 默认背景 )
    .el-menu-item {
      height: 44px;
      padding-left: 50px !important;
      background-color: white !important;
    }
  }

  :deep(.el-submenu__title) {
    background-color: #fff !important;
  }

  :deep(.el-menu-item) {
    box-sizing: border-box;
    margin: 20px auto;
    font-size: 16px;
    border-radius: 4px;

    &.is-active {
      font-weight: 500;

      .el-icon {
        color: white;
        border-radius: 4px;
        background-color: black;
      }

      &:hover {
        .el-icon {
          color: white;
        }
      }
    }

    &:hover {
      font-weight: 500;
      background: white;

      .el-icon {
        color: black;
      }
    }

    .el-icon {
      width: 38px;
      height: 38px;
      color: #41454d;
      border-radius: 4px;
      background-color: rgb(225, 225, 225);
    }

    span {
      line-height: 44px;
      margin-left: 20px;
    }
  }

  //缩小的menu样式
  .small-menu-item {
    justify-content: center;
    padding: 0;
    width: 44px;
    height: 44px;

    :deep(.el-icon) {
      margin-right: 0px;
    }
  }

  //放大的menu样式
  .big-menu-item {
    height: 44px;

    :deep(.el-icon) {
      margin-left: 30px;
    }

    span {
      line-height: 44px;
      margin-left: 18px;
    }
  }

  .line {
    width: 210px;
    height: 1px;
    margin: 0 auto;
    background-color: rgba(0, 0, 0, 0.1);
  }
}
</style>
