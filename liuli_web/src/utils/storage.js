export const setItem = (key, data) => {
  // 持久化数据（转化成json）
  if (typeof data === 'object') {
    data = JSON.stringify(data);
  }
  window.localStorage.setItem(key, data);
};

export const getItem = (key) => {
  // 获取数据
  const data = window.localStorage.getItem(key);
  try {
    return JSON.parse(data);
  } catch (err) {
    return data;
  }
};

export const removeItem = (key) => {
  // 删除数据
  window.localStorage.removeItem(key);
};

export const removeAllItem = (key) => {
  //删除所有数据
  window.localStorage.clear();
};
