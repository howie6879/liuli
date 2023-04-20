import { ICommonResp } from "@/api/shareInterface";

export interface ILoginParams {
    username: string;
    password: string;
}

export interface ILoginResp extends ICommonResp {
    data:{
        token: string;
        username: string;
    }
}

export interface IGetConfigParams {
    username: string;
}

export interface IGetConfigResp extends ICommonResp {
    data:{
        LL_X_TOKEN: string;
        _id: object;
    }
}
