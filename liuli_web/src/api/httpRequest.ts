import axios, { AxiosInstance } from 'axios';
import { ElNotification } from 'element-plus';
import { UserStore } from '@/store/user';
const axiosInstance: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 3000
});

axiosInstance.interceptors.request.use(
  // 请求拦截器
  (config) => {
    // 注入token
    const uerStore = UserStore(); 
    if (uerStore.token) {
      // 如果token存在 注入token
      config.headers!.Authorization = `Bearer ${uerStore.token}`;
    }
    // console.log(config);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  // 响应拦截器
  (response) => {
    // 此处 status 表示 http 请求状态码 200
    if (response.status == 200) {
      // 此处 status 表示服务端自定义的状态码
      const { data, info, status } = response.data;
      return {
        data: data,
        info: info,
        status: status
      };
    } else {
      console.log('非 200 响应', response.data);
      return Promise.reject(new Error(response.data));
    }
  },
  (error) => {
    // if (error.response && error.response.data && error.response.data.status === 401) {
    //     store.logout();
    // }
    const uerStore = UserStore(); 

    if (typeof error.response == 'undefined') {
      // 超时无响应
      console.log('服务器超时', error.response);
      return {
        data: {},
        info: '',
        status: 408
      };
    }

    if (error.response.status == 422 || error.response.status == 401) {
      // token 被篡改，格式错误
      ElNotification({
        message: error.response.data.msg,
        type: 'error',
        duration:2000
      });
      setTimeout(()=> uerStore.logout(), 3000);
    }
    return Promise.reject(error);
  }
);

const Request = {
  post<T = any>(url: string, data: object = {}): Promise<T> {
    try {
      return axiosInstance.post(url, data);
    } catch (error) {
      throw Error('请求失败');
    }
  },
};

export default Request;
