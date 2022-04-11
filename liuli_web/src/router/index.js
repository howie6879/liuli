import { createRouter, createWebHistory } from 'vue-router';

import Init from '../views/Init.vue';
import Home from '../views/Home.vue';

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/init',
        component: Init
    }
];

const router = createRouter({
    // history: createWebHashHistory(),
    history: createWebHistory('/'),
    routes
});

export default router;
