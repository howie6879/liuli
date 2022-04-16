import { createApp } from 'vue';

// 导入第三方库
import '@picocss/pico';
import pinia from './store/index';

// 导入路由实例
import router from './router/index';
import api from './api/index';
import App from './App.vue';

const app = createApp(App);
// 挂载 pinia
app.use(pinia);
// 挂载 axios 全局对象
app.provide('$api', api);
// 绑定
app.use(router).mount('#app');
