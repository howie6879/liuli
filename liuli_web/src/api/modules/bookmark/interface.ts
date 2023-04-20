import { IBookMark, ICommonResp, IPage } from "@/api/shareInterface";

export interface IUpdateBMParams extends IBookMark {
    username:string;
}

export interface IUpdateBMResp extends ICommonResp {
    data:{}
}

export interface IDeleteBMParams {
    username:string;
    url_list: string[];
}

export interface IDeleteBMResp extends ICommonResp {
    data:{}
}

export interface ISearchBMParams extends IBookMark, IPage {
    username:string;
}

export interface ISearchBMResp extends ICommonResp {
    data:{
        rows: IBookMark[];
        total: number;
    }
}

export interface IGetTagListParams {
    username:string;
    tag: string;
}

export interface IGetTagListResp extends ICommonResp {
    data:{tag:string;updated_at:number} []
}
