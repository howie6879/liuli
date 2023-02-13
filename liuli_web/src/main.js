import { createApp } from 'vue';

import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import svgIcon from '@/components/svgIcon';

// 导入 CSS 库
import './style/index.scss';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import 'virtual:svg-icons-register';

// 导入自定义模块
import api from './api/index';
import App from './App.vue';
import router from './router/index';
import pinia from './store/index';

const app = createApp(App);

app.component('SvgIcon', svgIcon);
// 挂载 router
app.use(router);
// 注册el-plus组件
app.use(ElementPlus);
// 注册el -icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}
// 挂载 pinia
app.use(pinia);
// 挂载 axios 全局对象
app.provide('$api', api);
// 绑定
app.mount('#app');
