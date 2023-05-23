import {
  IFavoriteArticleParams,
  IFavoriteArticleResp,
  IGetFavoriteParams,
  IGetFavoriteResp,
  IDeleteFavoriteArticleParams,
  IDeleteFavoriteArticleResp
 } from './interface';

import request from '@/api/httpRequest';

const favoriteApi = {
  // 根据doc_id收藏文章
  favoriteArticle: (params: IFavoriteArticleParams) => request.post<IFavoriteArticleResp>(`/favorite/article`, params),
  // 获取收藏文章
  getFavorite: (params: IGetFavoriteParams) => request.post<IGetFavoriteResp>(`/favorite/get`, params),
   // 根据doc_id 取消收藏文章
  deleteFavoriteArticle: (params: IDeleteFavoriteArticleParams) => request.post<IDeleteFavoriteArticleResp>(`/favorite/delete`, params),
};

export default favoriteApi;
