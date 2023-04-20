export interface ICommonResp{
    info: string;
    status: number;
}

export interface IPage {
    page: number;
    page_size: number;
}

export interface IBookMark {
    url: string;
    des: string;
    tags: string[];
    title: string;
    updated_at?:number;
}