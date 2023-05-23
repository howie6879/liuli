import {
  IGetConfigParams,
  IGetConfigResp,
  IUpdateConfigParams,
  IUpdateConfigResp,
 } from './interface';

import request from '@/api/httpRequest';

const configApi = {
  // 获取项目系统配置
  getConfig: (params: IGetConfigParams) => request.post<IGetConfigResp>(`/config/get`, params),
   // 更新项目系统配置
  updateConfig: (params: IUpdateConfigParams) => request.post<IUpdateConfigResp>(`/config/update`, params),

};

export default configApi;
