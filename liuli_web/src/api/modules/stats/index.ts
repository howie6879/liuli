import {IGetStatsParams,IGetStatsResp} from './interface';

import request from '@/api/httpRequest';

const statsApi = {
  // 获取所有文档源统计信息
  getStats: (params: IGetStatsParams) => request.post<IGetStatsResp>(`/stats/source_list`, params),
};

export default statsApi;
