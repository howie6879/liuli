import http from '../utils/axios';

export const userApi = {
  login(data) {
    // 用户登录函数
    return http({
      url: '/user/login',
      method: 'POST',
      data
    });
  },

  getStats(data) {
    return http({
      url: 'stats/source_list',
      method: 'POST',
      data
    });
  },

  tokenValid(data) {
    // 验证Token
    return http({
      url: '/user/token_valid',
      method: 'POST',
      data
    });
  }
};

export default userApi;
