import {IGetDocSourceParams,IGetDocSourceResp,IDeleteDocSourceParams,IDeleteDocSourceResp,IUpdateDocSourceParams,IUpdateDocSourceResp} from './interface';

import request from '@/api/httpRequest';

const docSourceApi = {
    // 根据doc_source获取订阅源配置
    getDocSource: (params: IGetDocSourceParams) => request.post<IGetDocSourceResp>(`/doc_source/get`, params),
    // 根据doc_source删除订阅源配置
    deleteDocSource: (params: IDeleteDocSourceParams) => request.post<IDeleteDocSourceResp>(`/doc_source/delete`, params),
    // 更新 doc_source
    updateDocSource: (params: IUpdateDocSourceParams) => request.post<IUpdateDocSourceResp>(`/doc_source/update`, params),
};

export default docSourceApi;
