import { ElNotification } from "element-plus";


// copy
export const copyUrl = async (data: string) => {
  try {
    await navigator.clipboard.writeText(data);
       ElNotification({
            message: '复制成功',
            duration: 2000,
            type: "success"
        })
  } catch (error) {
     ElNotification({
            message: '当前浏览器不支持读取剪贴板或无权限',
            duration: 2000,
            type: "warning"
        })
  }
};