import {  ICommonResp, IDocSource } from "@/api/shareInterface";

export interface IGetDocSourceParams {
    username:string;
    doc_source: string;
}

export interface IGetDocSourceResp extends ICommonResp {
    data: IDocSource[]
}

export interface IDeleteDocSourceParams {
    username:string;
    doc_source: string;
}

export interface IDeleteDocSourceResp extends ICommonResp {
    data:{} 
}

export interface IUpdateDocSourceParams extends IDocSource  {
}

export interface IUpdateDocSourceResp extends ICommonResp {
    data:{}
}


