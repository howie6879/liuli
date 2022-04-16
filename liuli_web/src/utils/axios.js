import axios from 'axios';

const http = axios.create({
    baseURL: '/v1',
    // baseURL: import.meta.env.VITE_APP_BASE_URL,
    timeout: 5000
});

http.interceptors.request.use(
    // 请求拦截器
    (config) => {
        // 注入token
        // if (store.getters.token) {
        // if (isTimeout()) {
        //     // 登出
        //     store.logout();
        //     return Promise.reject(new Error('token 失效'));
        // }
        // // 如果token存在 注入token
        // config.headers.Authorization = `Bearer ${store.getters.token}`;
        // }
        console.log(config);
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

http.interceptors.response.use(
    // 响应拦截器
    (response) => {
        const { data, info, status } = response.data;
        if (status == 200) {
            return data;
        } else {
            return Promise.reject(new Error(info));
        }
    },
    (error) => {
        if (error.response && error.response.data && error.response.data.status === 401) {
            store.logout();
        }
        return Promise.reject(error);
    }
);

export default http;
