import { ICommonResp,IPage,IArticle} from "@/api/shareInterface";

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

export interface IChangePwdParams {
    username: string;
    o_password: string;
    n_password: string;
}

export interface IChangePwdResp  extends ICommonResp {
     data:{}
}
