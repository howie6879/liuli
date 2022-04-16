import { defineStore } from 'pinia';

import api from '../api/index';
import store from '../store/index';
import { setLiuliToken, removeLiuliToken, getLiuliToken } from '../utils/auth';

export const useUserStore = defineStore('user', {
    state: () => {
        return { token: '', username: '' };
    },
    getters: {
        getToken: (state) => {
            return state.token || getLiuliToken().token;
        },
        getUsername: (state) => {
            return state.username || getLiuliToken().username;
        }
    },
    actions: {
        setToken(token, username) {
            this.token = token;
            this.username = username;
            setLiuliToken({
                token: token,
                username: username,
                timeStamp: Date.now()
            });
        },
        resetState() {
            this.token = '';
            this.username = '';
        },

        async login(data) {
            // 登录获取Token
            const res = await api.login(data);

            if (res && data.remember) {
                console.log('正在持久化 Token!');
                this.setToken(res.token, res.username);
            }
            return new Promise((resolve, reject) => {
                resolve(res);
            });
        },

        async logout() {
            this.resetState();
            removeLiuliToken();
        }
    }
});

export function callUserStore() {
    return useUserStore(store);
}
