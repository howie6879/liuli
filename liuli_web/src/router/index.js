import { createRouter, createWebHistory } from 'vue-router';

import Login from '../views/Login.vue';
import Home from '../views/Home.vue';

const routes = [
    {
        path: '/',
        component: Home,
        meta: { title: '首页' }
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

router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title || ''} - liuli.io`;
    next();
});

export default router;
