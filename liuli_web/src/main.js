import { createApp } from 'vue';

// 导入 CSS 库
import '../public/static/css/global.css';
import '../public/static/css/pico.min.css';

// 导入自定义模块
import api from './api/index';
import App from './App.vue';
import router from './router/index';
import pinia from './store/index';

const app = createApp(App);
// 挂载 router
app.use(router);
// 挂载 pinia
app.use(pinia);
// 挂载 axios 全局对象
app.provide('$api', api);
// 绑定
app.mount('#app');
