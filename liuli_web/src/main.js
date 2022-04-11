import { createApp } from 'vue';
import '@picocss/pico';

// 导入路由实例
import router from './router/index';
import App from './App.vue';

const app = createApp(App);

// vue实例上注册路由
app.use(router);
// 绑定
app.mount('#app');
