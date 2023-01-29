import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router';

import Login from '../views/Login.vue';
import Home from '../views/Home.vue';
import Subscription from '../views/Subscription.vue';
import Favorite from '../views/Favorite.vue';
import Bookmark from '../views/Bookmark.vue';
import Log from '../views/Log.vue';
import DocSource from '../views/DocSource.vue';
import { callUserStore } from '../store/user';

// 初始化 store
const userStore = callUserStore();

// 定义路由
const routes = [
  {
    path: '/',
    component: Home,
    meta: { title: '首页' }
  },
  {
    path: '/subscription',
    component: Subscription,
    meta: { title: '我的订阅' }
  },
  {
    path: '/bookmark',
    component: Bookmark,
    meta: { title: '我的订阅' }
  },
  {
    path: '/favorite',
    component: Favorite,
    meta: { title: '我的收藏' }
  },
  {
    path: '/doc_source',
    component: DocSource,
    meta: { title: '配置管理' }
  },
  {
    path: '/log',
    component: Log,
    meta: { title: '日志管理' }
  },
  {
    path: '/login',
    component: Login,
    meta: { title: '登录' }
  }
];

const router = createRouter({
  // history: createWebHashHistory(),
  history: createWebHistory('/'),
  routes
});

const whiteList = ['/login', '/404'];

router.beforeEach((to, from, next) => {
  if (to.meta && typeof to.meta.title !== 'undefined') {
    document.title = `${to.meta.title || ''} - liuli.io`;
  } else {
    document.title = `liuli.io`;
  }

  const hasToken = userStore.getToken;
  // console.log(userStore.getUsername + ' 已登录!');
  if (hasToken) {
    if (to.path == '/login') {
      // 登录状态下进入登录页面，直接跳转到主页
      next('/');
    } else {
      next();
    }
  } else {
    // 未登录状态直接进入登录页面
    if (whiteList.indexOf(to.path) > -1) {
      // 在白名单里直接跳转
      next();
    } else {
      // 非白名单一律跳到登录页
      next('/login');
    }
  }
});

export default router;
