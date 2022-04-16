import { defineStore } from 'pinia';

import api from '../api/index';
import store from '../store/index';
import { setLiuliToken, removeLiuliToken, getLiuliToken } from '../utils/auth';

export const useUserStore = defineStore('user', {
    state: () => {
        return { token: '' };
    },
    getters: {
        getToken: (state) => {
            // 获取storage的Token数据
            return state.token || getLiuliToken().token;
        }
    },
    actions: {
        setToken(token) {
            this.token = token;
            setLiuliToken({
                token: token,
                timeStamp: Date.now()
            });
        },

        async login(data) {
            // 登录获取Token
            const res = await api.login(data);
            if (res) {
                this.setToken(res.token);
            }
            return res;
        }
    }
});

export function callUserStore() {
    return useUserStore(store);
}
