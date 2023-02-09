import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router';

import Login from '../views/Login.vue';
import Subscription from '../views/Subscription.vue';
import Favorite from '../views/Favorite.vue';
import Bookmark from '../views/Bookmark.vue';
import Log from '../views/Log.vue';
import DocSource from '../views/DocSource.vue';
import Home from '@/views/Home.vue';
import { callUserStore } from '../store/user';

import Layout from '@/layout';
import subViews from '@/layout/components/subViews';

// 初始化 store
const userStore = callUserStore();

// 定义路由
export const routes = [
  {
    path: '/',
    component: Layout,
    name: 'index',
    redirect: '/home',
    children: [
      {
        path: 'home',
        component: Home,
        name: 'home',
        meta: { title: '首页', icon: 'svg-liuli_svg-side_bar-home' }
      },
      {
        path: 'Subscription',
        component: Subscription,
        name: 'Subscription',
        meta: { title: '我的订阅', icon: 'svg-liuli_svg-side_bar-subscription' }
      },
      {
        path: 'bookmark',
        component: Bookmark,
        name: 'Bookmark',
        meta: { title: '我的书签', icon: 'svg-liuli_svg-side_bar-link' }
      },
      {
        path: 'favorite',
        component: Favorite,
        name: 'Favorite',
        meta: { title: '我的收藏', icon: 'svg-liuli_svg-side_bar-favorite' }
      },
      {
        path: 'doc_source',
        component: DocSource,
        name: 'DocSource',
        meta: {
          title: '配置管理',
          icon: 'svg-liuli_svg-side_bar-spa' /* /src/assets/icons文件夹下的svg文件，文件夹名-文件名 */
        }
      },
      {
        path: 'log',
        component: Log,
        name: 'Log',
        meta: { title: '日志管理', icon: 'svg-liuli_svg-side_bar-log' }
      }
    ]
  },

  {
    path: '/login',
    component: Login,
    name: 'Login',
    isHidden: true, //是否显示
    meta: { title: '登录' }
  },
  {
    path: '/:catchAll(.*)',
    name: 'error',
    redirect: '/home',
    isHidden: true //是否显示
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
