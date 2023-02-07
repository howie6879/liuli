import path from 'path-browserify'

// 是否网址
export function isExternal(path) {
    return /^(https?:|mailto:|tel:)/.test(path)
  }

  
//拼接完整路径
export function resolvePath(routePath, basePath) {
  // 如果routePath是网址，直接返回routePath
  if (isExternal(routePath)) {
      return routePath
  }
  // 如果basePath是网址，直接返回basePath
  if (isExternal(basePath)) {
      return basePath
  }
  // 拼接完整路径
  return path.resolve(basePath, routePath)
}