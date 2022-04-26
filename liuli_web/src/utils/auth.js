import { setItem, getItem, removeItem } from '../utils/storage';

const TokenKey = 'x-auth-token';
const tokenTimeoutValue = 90 * 24 * 3600 * 1000;

export function isTokenTimeout(timeStamp) {
  // 判断是否超时
  const currentTime = Date.now();
  return currentTime - timeStamp > tokenTimeoutValue;
}

export function getLiuliToken() {
  // 使用前判断是否过期
  const tokenData = getItem(TokenKey);
  // 默认超时
  var isTimeout = true;
  if (tokenData) {
    // 存在 token，判断是否过期
    isTimeout = isTokenTimeout(tokenData.timeStamp);
  }
  // 超时重置，未超时继续使用
  return isTimeout ? { token: '', timeStamp: 0, username: '' } : tokenData;
}

export function setLiuliToken(tokenData) {
  return setItem(TokenKey, tokenData);
}

export function removeLiuliToken() {
  return removeItem(TokenKey);
}
