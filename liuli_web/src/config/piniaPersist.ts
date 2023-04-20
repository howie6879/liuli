import { PersistedStateOptions } from 'pinia-plugin-persistedstate';

/**
 * @description pinia持久化参数配置
 * @param {String} key 存储到持久化的 name
 * @param {string} persistType 数据持久化方式: sessionStorage | localStorage 默认localStorage
 * @return {persist}
 * */
const piniaPersistConfig = (
  key: string,
  persistType: 'sessionStorage' | 'localStorage' = 'localStorage',
): PersistedStateOptions => {
  const persist: PersistedStateOptions = {
    key,
    storage: persistType === 'localStorage' ? window.localStorage : window.sessionStorage,
  };
  return persist;
};

export default piniaPersistConfig;
