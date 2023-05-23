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

export interface IArticle {
    doc_id: string
    doc_author: string
    doc_date: string
    doc_des: string
    doc_html: string
    doc_image: string
    doc_keywords: string[]
    doc_link: string
    doc_name: string
    doc_source: string
    doc_source_account_intro: string
    doc_source_account_nick: string
    doc_source_meta_list: any[]
    doc_source_name: string
    doc_ts: number
    doc_type: string
}

export interface IDocSource {
  doc_source: string,
  doc_source_alias_name: string,
  username: string,
  author: string,
  backup: {
    backup_list: string[],
    query_days: number,
    delta_time: number,
    init_config: object,
    after_get_content: { 
        func: string,
        before_str: string,
        after_str: string
      }[]
  },
  collector: object,
  is_open: number,
  name: string,
  processor: {
    before_collect: object[],
    after_collect: object[]
  },
  schedule: {
    period_list: string[]
  },
  sender: {
    sender_list: string[],
    query_days: number,
    delta_time: number
  },
  updated_at: number
}