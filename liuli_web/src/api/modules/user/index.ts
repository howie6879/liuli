import {ILoginParams,ILoginResp,IGetConfigParams,IGetConfigResp} from './interface';

import request from '@/api/httpRequest';

const userApi = {
  // 登陆
  login: (params: ILoginParams) => request.post<ILoginResp>(`/user/login`, params),
  // 获取项目环境变量配置
  getConfig: (params: IGetConfigParams) => request.post<IGetConfigResp>(`/user/get_config`, params),
};

export default userApi;
