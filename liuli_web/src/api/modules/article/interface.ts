import {  ICommonResp, IPage,IArticle } from "@/api/shareInterface";

export interface IGetArticleParams {
    username:string;
    doc_id: string;
}

export interface IGetArticleResp extends ICommonResp {
    data:{
        doc_core_html: string
    }&IArticle 
}


export interface ISearchArticleParams extends  IPage {
    username:string;
    doc_source: string,
    doc_source_name: string ,
    doc_name: string,
    doc_type: string,
}

export interface ISearchArticleResp extends ICommonResp {
    data:{
        rows: IArticle[];
        total: number;
    }
}

export interface IFavoriteArticleParams {
    username:string;
    doc_id: string;
}

export interface IFavoriteArticleResp extends ICommonResp {
    data:{} 
}

