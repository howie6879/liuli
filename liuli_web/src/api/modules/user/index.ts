import {
  ILoginParams,
  ILoginResp,
 
  IChangePwdParams,
  IChangePwdResp,
  } from './interface';

import request from '@/api/httpRequest';

const userApi = {
  // 登陆
  login: (params: ILoginParams) => request.post<ILoginResp>(`/user/login`, params),
  // 修改密码
  changePwd: (params: IChangePwdParams) => request.post<IChangePwdResp>(`/user/change_pwd`, params),
 
};

export default userApi;
