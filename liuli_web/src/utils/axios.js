import axios from 'axios';
import { getLiuliToken } from './auth';

const http = axios.create({
  baseURL: '/v1',
  // baseURL: import.meta.env.VITE_APP_BASE_URL,
  timeout: 3000
});

http.interceptors.request.use(
  // 请求拦截器
  (config) => {
    // 注入token
    if (getLiuliToken().token) {
      // 如果token存在 注入token
      config.headers.Authorization = `Bearer ${store.getters.token}`;
    }
    // console.log(config);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

http.interceptors.response.use(
  // 响应拦截器
  (response) => {
    return response.data;
    // const { data, info, status } = response.data;
    // console.log(response.data);
    // if (status == 200) {
    //   return data;
    // } else {
    //   return Promise.reject(new Error(info));
    // }
  },
  (error) => {
    // if (error.response && error.response.data && error.response.data.status === 401) {
    //     store.logout();
    // }
    if (typeof error.response == 'undefined') {
      // 超时无响应
      console.log('服务器超时', error.status);
      return {
        data: {},
        info: '',
        status: 408
      };
    } else {
      return Promise.reject(error);
    }
  }
);

export default http;
