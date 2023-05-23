import { defineStore,storeToRefs } from 'pinia';
import piniaPersistConfig from '@/config/piniaPersist';
import { ref } from 'vue';
import { userApi } from '@/api';
import { ILoginParams } from '@/api/modules/user/interface'

export const UserStore = defineStore(
  'liuli-user-store-id',
  () => {
    const token = ref('',);
    const username=ref('');

    const login = async (data:ILoginParams)=>{
      const res= await userApi.login(data)
      if(res.status==200){
        token.value = res.data.token
        username.value = res.data.username
      }
      return res;
    }

    const logout= ()=>{
      token.value = ''
      username.value = ''
      window.location.href = '/login'
    }

   

  
    return {
      token,
      username,
      login,
      logout,
    };
  },
  { persist: piniaPersistConfig('liuli-user-store-id') },
);

export const useUserStore = () => storeToRefs(UserStore());



// export const useUserStore = defineStore('user', {
//   state: () => {
//     return { token: '', username: '' };
//   },
//   getters: {
//     getToken: (state) => {
//       return state.token;
//     },
//     getUsername: (state) => {
//       return state.username;
//     }
//   },
//   actions: {
//     setToken(token: string, username: string) {
//       this.token = token;
//       this.username = username;
//       setLiuliToken(state)
//     },
//     resetState() {
//       this.token = '';
//       this.username = '';
//       setLiuliToken(state)
//     },

//     async login(data: { username: any; password: any; }) {
//       // 登录获取 Token
//       const res = await api.login(data);
//       if (res.status == 200) {
//         console.log('正在持久化 Token!');
//         this.setToken(res.data.token, res.data.username);
//       }
//       return new Promise((resolve, reject) => {
//         resolve(res);
//       });
//     },

//     async logout() {
//       this.resetState();
//       removeLiuliToken();
//     }
//   }
// });
