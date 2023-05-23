import { ICommonResp,IPage,IArticle} from "@/api/shareInterface";

export interface IFavoriteArticleParams {
    username:string;
    doc_id: string;
}

export interface IFavoriteArticleResp extends ICommonResp {
    data:{} 
}

export interface IGetFavoriteParams extends IPage {
    username: string;
}

export interface IGetFavoriteResp extends ICommonResp {
    data:{
        rows: IArticle[]
        total: number;
    }
}

export interface IDeleteFavoriteArticleParams {
    username:string;
    doc_id_list: string[];
}

export interface IDeleteFavoriteArticleResp extends ICommonResp {
    data:{} 
}

