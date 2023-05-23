import {IGetArticleParams,IGetArticleResp,ISearchArticleParams,ISearchArticleResp,} from './interface';

import request from '@/api/httpRequest';

const articleApi = {
    // 根据doc_id获取文章详情
    getArticle: (params: IGetArticleParams) => request.post<IGetArticleResp>(`/articles/get`, params),
    // 分页查询文章
    searchArticle: (params: ISearchArticleParams) => request.post<ISearchArticleResp>(`/articles/search`, params),
};

export default articleApi;
