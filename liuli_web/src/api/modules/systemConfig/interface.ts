import { ICommonResp,IPage,IArticle} from "@/api/shareInterface";

export interface IGetConfigParams {
    username: string;
}

export interface IGetConfigResp extends ICommonResp {
    data:{
        LL_X_TOKEN: string;
        _id: object;
    }
}

export interface IUpdateConfigParams {
    username: string;
    data: object;
}

export interface IUpdateConfigResp extends ICommonResp {
    data:{}
}


