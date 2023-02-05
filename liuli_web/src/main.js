import { createApp } from 'vue';

// 导入 CSS 库
// import '/public/static/css/global.css';
import '../public/static/css/pico.min.css';
// import '@picocss/pico';
import '../public/static/css/global.css';

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


// 导入自定义模块
import api from './api/index';
import App from './App.vue';
import router from './router/index';
import pinia from './store/index';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// import install  from './assets/icons/index'

import 'virtual:svg-icons-register'
const app = createApp(App);

import svgIcon from '@/components/svgIcon'
app.component('SvgIcon', svgIcon)
// 挂载 router
app.use(router);
// 注册el-plus组件
app.use(ElementPlus)
// 注册el -icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
// 挂载 pinia
app.use(pinia);
// 挂载 axios 全局对象
app.provide('$api', api);
// 绑定
app.mount('#app');
