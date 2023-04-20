<template>
  <sidebar-menu :menu="sideBarConfig.menu" @update:collapsed="onToggleCollapse" :theme="sideBarConfig.theme"
    :width="sideBarConfig.width" :hideToggle="sideBarConfig.hideToggle" :relative="false" :disableHover="true" />
</template>

<script setup lang="ts">
import { SidebarMenu } from 'vue-sidebar-menu';
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css';
import '@fortawesome/fontawesome-free/css/all.css';
import { ref, h } from 'vue';

const sideBarConfig = ref({
  width: '250px',
  hideToggle: false,
  collapsed: false,
  theme: 'white-theme',
  menu: [
    {
      header: 'LiuLi',
      hiddenOnCollapse: false
    },
    {
      href: '/',
      title: '首页',
      icon: 'fa-solid fa-house-chimney-window'
    },
    {
      href: '/subscription',
      title: '我的订阅',
      icon: 'fa-solid fa-book-open-reader'
    },
    {
      href: '/bookmark',
      title: '我的书签',
      icon: 'fa-solid fa-link'
    },
    {
      href: '/favorite',
      title: '我的收藏',
      icon: 'fa-solid fa-crown'
    },
    {
      component: h('hr', {
        style: {
          margin: '20px',
          border: '0',
          'background-color': 'rgba(0, 0, 0, 0.1)',
          height: '2px'
        }
      })
    },
    // {
    //   header: '设置',
    //   hiddenOnCollapse: true
    // },
    {
      href: '/doc_source',
      title: '配置管理',
      icon: 'fa fa-spa'
    },
    {
      href: '/log',
      title: '日志管理',
      icon: 'fa-solid fa-chart-simple'
    }
  ]
});

const emits = defineEmits(['menuStatus']);

const onToggleCollapse = function (collapsed) {
  // 参考：https://blog.csdn.net/skyblue_afan/article/details/126667586
  emits('menuStatus', collapsed);
};
</script>

<style>
li.vsm--header {
  color: black !important;
  font-size: 16px !important;
  font-weight: 200;
}

ul li {
  list-style: none;
}

button {
  border-radius: 0px;
  margin-bottom: 0px;
}

button:focus {
  box-shadow: none;
}

.v-sidebar-menu.vsm_white-theme .vsm--link_level-1.vsm--link_active {
  -webkit-box-shadow: 3px 0px 0px 0px #e2989e inset;
  box-shadow: 3px 0 #e2989e inset;
}

.vsm--toggle-btn {
  height: 50px !important;
  background-color: #d0d0d0 !important;
}
</style>
