import { createApp } from 'vue';

// 导入第三方库
import '@picocss/pico';

// 导入自定义模块
import App from './App.vue';
import api from './api/index';
import pinia from './store/index';
import router from './router/index';

const app = createApp(App);
// 挂载 pinia
app.use(pinia);
// 挂载 axios 全局对象
app.provide('$api', api);
// 绑定
app.use(router).mount('#app');
