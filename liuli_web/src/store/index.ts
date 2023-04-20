import { createPinia, defineStore, storeToRefs } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

export const GlobalStore = defineStore('liuli-global-store-id',()=>{
    
})

export const useGlobalStore = () => storeToRefs(GlobalStore());

// piniaPersist(持久化)
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

export default pinia;
