import http from '../utils/axios';

const userApi = {
    login(data) {
        // 用户登录函数
        return http({
            url: '/user/login',
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
