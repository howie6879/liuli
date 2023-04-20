import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import svgIcon from '@/components/svgIcon/index.vue';

// 导入 CSS 库
import './style/index.scss';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import 'virtual:svg-icons-register';

// 导入自定义模块
import App from '@/App.vue'
import router from '@/router';
import pinia from '@/store';
import { createApp } from 'vue';
import dayjs from 'dayjs'; // 时间格式化库
import 'dayjs/locale/zh-cn'; // import locale
import relativeTime from 'dayjs/plugin/relativeTime'  //相对时间插件


const app = createApp(App);

app.component('SvgIcon', svgIcon);

dayjs.locale('zh-cn'); // use locale
dayjs.extend(relativeTime)

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
// 绑定
app.mount('#app');
