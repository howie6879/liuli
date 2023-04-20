import {IUpdateBMParams,IUpdateBMResp,IDeleteBMParams,IDeleteBMResp,ISearchBMParams,ISearchBMResp,IGetTagListParams,IGetTagListResp} from './interface';

import request from '@/api/httpRequest';

const bookmarkApi = {
    // 更新书签
    updateBM: (params: IUpdateBMParams) => request.post<IUpdateBMResp>(`/bm/update`, params),
    // 删除书签
    deleteBM: (params: IDeleteBMParams) => request.post<IDeleteBMResp>(`/bm/delete_url`, params),
    // 分页查询书签
    searchBM: (params: ISearchBMParams) => request.post<ISearchBMResp>(`/bm/search`, params),
    // 获取 tag 列表
    getTagList: (params: IGetTagListParams) => request.post<IGetTagListResp>(`/bm/get_tag_list`, params),


    // 测试bm 接口状态
    testStatus:(params: {}) => request.post<IUpdateBMResp>(`/bm/status`, params),


};

export default bookmarkApi;
